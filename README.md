# Django E-commerce Website

This project is a simple e-commerce website developed using Django, a high-level Python web framework. It provides functionalities for user registration/authentication, user profile management, product management, shopping cart, order processing, and more.

## Features

- **User Registration & Authentication:** Users can create new accounts, log in, and log out securely. Passwords are encrypted for security.
- **User Profile Management:** Users can update their profile information and manage their profile picture.
- **Product Management:** Admins can add, edit, and delete products with details such as name, description, price, and image.
- **Shopping Cart:** Users can add products to their cart, view the cart, update quantities, remove items, and see the total price.
- **Order Processing:** Users can place orders, and admins can manage and fulfill orders. Order details are securely stored in the database.
- **Database Integration:** Uses a relational database (SQLite, MySQL, PostgreSQL, etc.) to store and retrieve user information, product data, and order details.


## Installation

To install and run Fringe locally on your machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/atharvt17/epharma-django
   ```
2. **Navigate to the Directory**:
   ```bash
   cd ecom
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Development Server**:
   ```bash
   http://localhost:8000/
   ```

## Usage

- Visit the website in your browser: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin` (Use superuser credentials)

## Folder Structure
```bash
ecom
│   db.sqlite3
│   manage.py
│
├───ecom
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│  
└───pharmacy
    │   admin.py
    │   apps.py
    │   forms.py
    │   models.py
    │   tests.py
    │   urls.py
    │   views.py
    │   __init__.py
    │
    │
    ├───templates
    │       Account-info.html
    │       billing_address.html
    │       carts.html
    │       dashboard.html
    │       login.html
    │       orders.html
    │       ordersmanager.html
    │       order_confirmation.html
    │       place_order.html
    │       product_detail.html
    │       product_page.html
    │       registration.html
    │       shipping_address.html
    │
└───product_images
```

## Technologies Used

- **Django:** Backend framework for web development.
- **HTML/CSS/JavaScript:** Frontend languages for building user interfaces
