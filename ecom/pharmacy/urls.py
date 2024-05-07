from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('login_view', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('signup_view', views.signup_view, name='signup_view'),
    path('products/', views.product_page, name='product_page'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('carts', views.carts, name='carts'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.orders, name='orders'),

    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('accountinfo', views.accountinfo, name='accountinfo'),
    path('productpage', views.productpage, name='productpage'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('fetch-shipping-addresses/',views.fetch_shipping_addresses, name='fetch_shipping_addresses'),
    path('save-shipping-address/', views.save_shipping_address, name='save_shipping_address'),
    path('delete-shipping-address/<int:address_id>/', views.delete_shipping_address, name='delete_shipping_address'),
    path('ordersmanager/', views.orders_manager, name='ordersmanager'),
    path('place_order_and_update',views.place_order_and_update, name='place_order_and_update'),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)