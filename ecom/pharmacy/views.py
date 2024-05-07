from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Product,Cart,ShippingAddress,Order, OrderItem
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.db.models import Sum



@login_required
def orders_manager(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        order = Order.objects.get(pk=order_id)
        order.status = new_status
        order.save()
        
    orders = Order.objects.all().annotate(total_price=Sum('orderitem__price'))
    return render(request, 'ordersmanager.html', {'orders': orders})


def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order = get_object_or_404(Order, pk=order_id)
        order.status = new_status
        order.save()
        return redirect('ordersmanager')
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_shipping_address(request, address_id):
    try:
        # Retrieve the shipping address from the database
        shipping_address = ShippingAddress.objects.get(id=address_id)
        # Delete the shipping address
        shipping_address.delete()
        # Return success response
        return JsonResponse({'success': True})
    except ShippingAddress.DoesNotExist:
        # Return error response if shipping address not found
        return JsonResponse({'success': False, 'error': 'Shipping address not found'})

def save_shipping_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')

        # Save shipping address to the database
        shipping_address = ShippingAddress.objects.create(
            name=name,
            contact=contact,
            address=address,
            address2=address2,
            city=city,
            pincode=pincode,
            state=state
        )
        print(shipping_address.contact)
        # Return success response
        return JsonResponse({'success': True})

    # Return error response if the request method is not POST
    return JsonResponse({'success': False})

def fetch_shipping_addresses(request):
    addresses = ShippingAddress.objects.all().values()
    return JsonResponse(list(addresses), safe=False)

from django.contrib.auth.decorators import login_required

@login_required
def place_order(request):
    cart_items = Cart.objects.all()
    total_amount = sum(item.price for item in cart_items)
    return render(request, 'place_order.html',{'total_amount':total_amount})

import json

@login_required
@require_POST
@transaction.atomic
def place_order_and_update(request):
    try:
        body = request.body
        data = json.loads(body)
        shipping_address_id = data.get('shipping_address_id')
        cart_items = Cart.objects.filter(user=request.user)

        # Retrieve shipping address details
        shipping_address = ShippingAddress.objects.get(id=shipping_address_id)
        
        # Create a new order
        order = Order.objects.create(user=request.user, shipping_address=shipping_address,contact=shipping_address.contact)

        # Create order items from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price
            )

        # Clear the user's cart after placing the order
        cart_items.delete()

        return JsonResponse({'success': True, 'message': 'Order placed successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})




@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')


@login_required
def orders(request):
    orders = Order.objects.all()
    for order in orders:
        total_price = sum(item.price for item in order.orderitem_set.all())
        order.total_price = total_price  
    return render(request, 'orders.html', {'orders': orders})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('carts')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        price = product.price
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'price': price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.price = cart_item.product.price * cart_item.quantity
            cart_item.save()
        return JsonResponse({'message': 'Product added to cart'})
    else:
        return JsonResponse({'error': 'Invalid request method'})



def product_page(request):
    products = Product.objects.all()
    return render(request, 'product_page.html', {'products': products})


@login_required
def carts(request):
    cart_items = Cart.objects.all()
    total_amount = sum(item.price for item in cart_items)
    return render(request, 'carts.html', {'cart_items': cart_items, 'total_amount': total_amount})


User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fullname.split()[0] 
            user.last_name = ' '.join(fullname.split()[1:])  
            user.save()

            print("Registration successful")

            return redirect('/')
        
        except IntegrityError:
            return render(request, 'registration.html', {'error_message': 'Username or email already exists. Please choose a different username or email.'})
    else:
        return render(request, 'registration.html')



def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user) 
            
            if username == 'ordermanager':
                # Redirect to the staff page
                return redirect('/ordersmanager')
            else:
                # Redirect to dashboard
                return redirect('/dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

    
def register(request):
    return render(request, 'registration.html')
    

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def productpage(request):
    return render(request, 'product_page.html')



@login_required
def logout_view(request):
    logout(request)
    
    return redirect('/')




@login_required
def accountinfo(request):
    user = request.user
    
    fullname = user.get_full_name()
    
    return render(request, 'Account-info.html', {'fullname': fullname})

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        if name:
            user.first_name = name.split()[0]
            user.last_name = ' '.join(name.split()[1:])

        if email:
            user.email = email

        if username:
            user.username = username

        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})