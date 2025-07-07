"""
PageForge - Premium Digital Bookstore
Developed by Mahender Banoth (IIT Patna)
Instagram: @mahender_hustles
LinkedIn: Mahender Hustles
GitHub: mahenderoffl

A Flask-based e-commerce platform for digital books with admin management,
user authentication, shopping cart, and premium UI design.

Development Setup:
- Run database_setup.py to initialize the database with sample data
- Default accounts are created during setup (check database_setup.py for details)
- IMPORTANT: Change default passwords before deploying to production
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

import psycopg2
import psycopg2.extras
import os

def get_connection():
    return psycopg2.connect(
        "postgres://postgres@y4ggc1whzgb37xwm.browser.db.build/postgres?sslmode=require",
        cursor_factory=psycopg2.extras.RealDictCursor
    )

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey123")

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT role FROM Users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not user or user['role'] != 'Admin':
                flash('Admin access required.', 'error')
                return redirect(url_for('home'))
        except Exception:
            flash('Error checking permissions.', 'error')
            return redirect(url_for('home'))
            
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Show more books and order by book_id to show newest first
        cursor.execute("SELECT * FROM Books WHERE stock > 0 ORDER BY book_id DESC LIMIT 12")
        books = cursor.fetchall()
        
        # Debug: Print book count and sample data
        print(f"Found {len(books)} books in database")
        if books:
            print(f"Sample book: {books[0]['title']} by {books[0]['author']}")
        
        cursor.close()
        conn.close()
        return render_template("index.html", books=books)
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return render_template("index.html", books=[])

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get and validate form data
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Debug logging
            print(f"DEBUG: Registration attempt - Username: {username}, Email: {email}")
            
            # Basic validation
            if not username or not email or not password:
                flash('All fields are required.', 'error')
                return render_template('register.html')
            
            # Username validation
            if len(username) < 3:
                flash('Username must be at least 3 characters long.', 'error')
                return render_template('register.html')
            
            if len(username) > 50:
                flash('Username must be less than 50 characters.', 'error')
                return render_template('register.html')
            
            # Check username format
            import re
            if not re.match(r'^[a-zA-Z0-9_-]+$', username):
                flash('Username can only contain letters, numbers, underscores, and hyphens.', 'error')
                return render_template('register.html')
            
            # Email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                flash('Please enter a valid email address.', 'error')
                return render_template('register.html')
            
            # Password confirmation check
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('register.html')
            
            # Enhanced password validation
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('register.html')
            
            if len(password) > 128:
                flash('Password must be less than 128 characters.', 'error')
                return render_template('register.html')
            
            # Password strength requirements
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            
            if not (has_upper and has_lower and has_digit):
                flash('Password must contain at least one uppercase letter, one lowercase letter, and one number.', 'error')
                return render_template('register.html')
            
            # Database operations
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if username already exists (case-insensitive)
            cursor.execute("SELECT id FROM Users WHERE LOWER(username) = LOWER(%s)", (username,))
            if cursor.fetchone():
                flash('Username already exists. Please choose a different username.', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            
            # Check if email already exists
            cursor.execute("SELECT id FROM Users WHERE LOWER(email) = LOWER(%s)", (email,))
            if cursor.fetchone():
                flash('Email already registered. Please use a different email or try logging in.', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            
            # Create new user with current timestamp
            password_hash = generate_password_hash(password)
            cursor.execute(
                """INSERT INTO Users (username, email, password_hash, role, created_at) 
                   VALUES (%s, %s, %s, 'Customer', NOW())""",
                (username, email, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            
            print(f"DEBUG: User created successfully with ID: {user_id}")
            
            # Log user activity if analytics tables exist
            try:
                cursor.execute("""
                    INSERT INTO user_activities (user_id, activity_type, activity_description, ip_address, timestamp)
                    VALUES (%s, 'registration', %s, %s, NOW())
                """, (user_id, f'User registered with email {email}', request.remote_addr or '127.0.0.1'))
                conn.commit()
                print("DEBUG: User activity logged")
            except mysql.connector.Error as analytics_error:
                print(f"DEBUG: Analytics tables not available - skipping activity log: {analytics_error}")
                pass
            
            cursor.close()
            conn.close()
            
            flash('Registration successful! Welcome to PageForge. Please log in with your new account.', 'success')
            return redirect(url_for('login'))
            
        except mysql.connector.Error as db_error:
            print(f"Database error during registration: {db_error}")
            flash('Registration failed due to a database error. Please try again.', 'error')
            return render_template('register.html')
        
        except Exception as general_error:
            print(f"General error during registration: {general_error}")
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    # GET request - show registration form
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash(f'Welcome back, {user["username"]}!', 'success')
                
                # Redirect to admin dashboard if admin
                if user['role'] == 'Admin':
                    return redirect(url_for('admin_books'))
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.', 'error')
                
        except mysql.connector.Error as e:
            flash('Login failed. Please try again.', 'error')
            print(f"Login error: {e}")
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route("/add_to_cart/<int:book_id>")
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    book_id_str = str(book_id)
    
    if book_id_str in cart:
        cart[book_id_str] += 1
    else:
        cart[book_id_str] = 1
    
    session['cart'] = cart
    flash('Book added to cart!', 'success')
    return redirect(url_for('home'))

@app.route("/cart")
def cart():
    cart_items = []
    total = 0.0
    
    if 'cart' in session and session['cart']:
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            for book_id, quantity in session['cart'].items():
                cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
                book = cursor.fetchone()
                if book:
                    # Convert decimal to float to avoid type issues
                    price = safe_float(book['price'])
                    item_total = price * quantity
                    cart_items.append({
                        'book': book,
                        'quantity': quantity,
                        'total': item_total
                    })
                    total += item_total
            
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            flash('Error loading cart.', 'error')
            print(f"Cart error: {e}")
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        address = request.form['address']
        phone = request.form['phone']
        payment_method = request.form['payment_method']
        
        if not address or not phone:
            flash('Address and phone are required.', 'error')
            return render_template('checkout.html')
        
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Calculate total
            total = 0.0
            for book_id, quantity in session['cart'].items():
                cursor.execute("SELECT price FROM Books WHERE book_id = %s", (book_id,))
                book = cursor.fetchone()
                if book:
                    # Convert decimal to float to avoid type issues
                    price = safe_float(book['price'])
                    total += price * quantity
            
            # Create order
            cursor.execute(
                """INSERT INTO Orders (user_id, total_amount, shipping_address, phone, payment_method) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (session['user_id'], total, address, phone, payment_method)
            )
            order_id = cursor.lastrowid
            
            # Add order items
            for book_id, quantity in session['cart'].items():
                cursor.execute("SELECT price FROM Books WHERE book_id = %s", (book_id,))
                book = cursor.fetchone()
                if book:
                    cursor.execute(
                        """INSERT INTO Order_Items (order_id, book_id, quantity, price) 
                           VALUES (%s, %s, %s, %s)""",
                        (order_id, book_id, quantity, book['price'])
                    )
                    
                    # Update stock
                    cursor.execute(
                        "UPDATE Books SET stock = stock - %s WHERE book_id = %s",
                        (quantity, book_id)
                    )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Clear cart
            session.pop('cart', None)
            flash('Order placed successfully!', 'success')
            return redirect(url_for('my_library'))
            
        except mysql.connector.Error as e:
            flash('Checkout failed. Please try again.', 'error')
            print(f"Checkout error: {e}")
    
    return render_template('checkout.html')

@app.route("/my-library")
@login_required
def my_library():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.order_id, o.order_date, o.status, b.title, b.author, b.image_url, oi.quantity
            FROM Orders o
            JOIN Order_Items oi ON o.order_id = oi.order_id
            JOIN Books b ON oi.book_id = b.book_id
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
        """, (session['user_id'],))
        library_books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('my_library.html', books=library_books)
    except mysql.connector.Error as e:
        flash('Error loading library.', 'error')
        print(f"Library error: {e}")
        return render_template('my_library.html', books=[])

@app.route("/admin/books")
@admin_required
def admin_books():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Use book_id instead of created_at for ordering since created_at might not exist
        cursor.execute("SELECT * FROM Books ORDER BY book_id DESC")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admin_books.html', books=books)
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        print(f"Admin books error: {e}")
        return render_template('admin_books.html', books=[])

@app.route("/admin/books/add", methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        print("DEBUG: POST request received for add_book")
        
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        price_str = request.form.get('price', '0')
        stock_str = request.form.get('stock', '0')
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        print(f"DEBUG: Form data - Title: {title}, Author: {author}, Category: {category}, Price: {price_str}, Stock: {stock_str}")
        
        # Validation
        if not title or not author or not category:
            print("DEBUG: Validation failed - missing required fields")
            flash('Title, author, and category are required fields.', 'error')
            return render_template('book_form.html', book=None)
        
        try:
            price = float(price_str) if price_str else 0.0
            stock = int(stock_str) if stock_str else 0
            print(f"DEBUG: Converted price: {price}, stock: {stock}")
        except ValueError:
            print("DEBUG: Validation failed - invalid price or stock format")
            flash('Price and stock must be valid numbers.', 'error')
            return render_template('book_form.html', book=None)
        
        if price < 0 or stock < 0:
            print("DEBUG: Validation failed - negative values")
            flash('Price and stock cannot be negative.', 'error')
            return render_template('book_form.html', book=None)
        
        try:
            print("DEBUG: Attempting database insertion")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO Books (title, author, price, stock, category, description, image_url) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (title, author, price, stock, category, description, image_url)
            )
            conn.commit()
            book_id = cursor.lastrowid
            print(f"DEBUG: Book inserted successfully with ID: {book_id}")
            cursor.close()
            conn.close()
            
            flash('Book added successfully!', 'success')
            return redirect(url_for('admin_books'))
        except mysql.connector.Error as e:
            print(f"DEBUG: Database error: {e}")
            flash(f'Database error: {str(e)}', 'error')
            return render_template('book_form.html', book=None)
    
    print("DEBUG: GET request for add_book form")
    return render_template('book_form.html', book=None)

@app.route("/admin/books/edit/<int:book_id>", methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        price_str = request.form.get('price', '0')
        stock_str = request.form.get('stock', '0')
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        # Debug logging
        print(f"DEBUG: Editing book {book_id}")
        print(f"DEBUG: Form data - Title: {title}, Author: {author}")
        print(f"DEBUG: Image URL received: '{image_url}'")
        print(f"DEBUG: Description: '{description}'")
        
        # Validation
        if not title or not author or not category:
            flash('Title, author, and category are required fields.', 'error')
            return redirect(url_for('edit_book', book_id=book_id))
        
        try:
            price = float(price_str) if price_str else 0.0
            stock = int(stock_str) if stock_str else 0
        except ValueError:
            flash('Price and stock must be valid numbers.', 'error')
            return redirect(url_for('edit_book', book_id=book_id))
        
        if price < 0 or stock < 0:
            flash('Price and stock cannot be negative.', 'error')
            return redirect(url_for('edit_book', book_id=book_id))
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Debug: Check current image_url before update
            cursor.execute("SELECT image_url FROM Books WHERE book_id = %s", (book_id,))
            current_book = cursor.fetchone()
            print(f"DEBUG: Current image_url in DB: '{current_book[0] if current_book else 'None'}'")
            
            cursor.execute(
                """UPDATE Books SET title=%s, author=%s, price=%s, stock=%s, 
                   category=%s, description=%s, image_url=%s WHERE book_id=%s""",
                (title, author, price, stock, category, description, image_url, book_id)
            )
            conn.commit()
            
            # Debug: Check image_url after update
            cursor.execute("SELECT image_url FROM Books WHERE book_id = %s", (book_id,))
            updated_book = cursor.fetchone()
            print(f"DEBUG: Updated image_url in DB: '{updated_book[0] if updated_book else 'None'}'")
            
            cursor.close()
            conn.close()
            
            flash('Book updated successfully!', 'success')
            return redirect(url_for('admin_books'))
        except mysql.connector.Error as e:
            flash(f'Database error: {str(e)}', 'error')
            print(f"Edit book error: {e}")
            return redirect(url_for('edit_book', book_id=book_id))
    
    # Get book for editing
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not book:
            flash('Book not found.', 'error')
            return redirect(url_for('admin_books'))
            
        return render_template('book_form.html', book=book)
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        print(f"Edit book load error: {e}")
        return redirect(url_for('admin_books'))

@app.route("/admin/books/delete/<int:book_id>")
@admin_required
def delete_book(book_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Book deleted successfully!', 'success')
    except mysql.connector.Error as e:
        flash('Error deleting book.', 'error')
        print(f"Delete book error: {e}")
    
    return redirect(url_for('admin_books'))

@app.route("/admin/analytics")
@admin_required
def admin_analytics():
    """Admin analytics dashboard with comprehensive user and traffic data"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Basic user statistics
        cursor.execute("SELECT COUNT(*) as total FROM Users")
        total_users = cursor.fetchone()['total']
        
        # Check if created_at column exists, if not use a default approach
        cursor.execute("SHOW COLUMNS FROM Users LIKE 'created_at'")
        has_created_at = cursor.fetchone() is not None
        
        if has_created_at:
            cursor.execute("SELECT COUNT(*) as count FROM Users WHERE created_at >= CURDATE()")
            new_users_today = cursor.fetchone()['count']
        else:
            new_users_today = 0  # Default when no created_at column
        
        cursor.execute("SELECT COUNT(*) as count FROM Users WHERE role = 'Customer'")
        customer_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM Users WHERE role = 'Admin'")
        admin_count = cursor.fetchone()['count']
        
        # Check if created_at column exists, if not use a default approach
        cursor.execute("SHOW COLUMNS FROM Users LIKE 'created_at'")
        has_created_at = cursor.fetchone() is not None
        
        if has_created_at:
            # Registration trends (last 30 days)
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count 
                FROM Users 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                GROUP BY DATE(created_at)
                ORDER BY date
            """)
            registration_data = cursor.fetchall()
            
            # Recent users (without Orders dependency)
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.role, u.created_at
                FROM Users u
                WHERE u.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                ORDER BY u.created_at DESC
                LIMIT 10
            """)
            recent_users = cursor.fetchall()
        else:
            # Fallback for tables without created_at column
            registration_data = []
            cursor.execute("""
                SELECT u.id, u.username, u.email, u.role
                FROM Users u
                ORDER BY u.id DESC
                LIMIT 10
            """)
            recent_users = cursor.fetchall()
        
        # Password security analysis (simulated - in real app you'd analyze password complexity)
        strong_passwords = max(1, int(total_users * 0.7))  # Simulate 70% strong
        medium_passwords = max(0, int(total_users * 0.2))  # Simulate 20% medium
        weak_passwords = max(0, total_users - strong_passwords - medium_passwords)
        
        # Traffic simulation (in real app, you'd track actual page views)
        import random
        from datetime import datetime, timedelta
        
        # Generate simulated traffic data for last 7 days
        traffic_labels = []
        traffic_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=6-i)).strftime('%m/%d')
            traffic_labels.append(date)
            traffic_data.append(random.randint(50, 200))
        
        # Registration chart data
        registration_labels = []
        reg_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=6-i)).strftime('%m/%d')
            registration_labels.append(date)
            reg_data.append(random.randint(0, 5))
        
        # Simulated popular pages
        popular_pages = [
            {'url': '/', 'title': 'Home Page', 'views': 1250, 'percentage': 100},
            {'url': '/browse', 'title': 'Browse Books', 'views': 890, 'percentage': 71},
            {'url': '/login', 'title': 'Login Page', 'views': 650, 'percentage': 52},
            {'url': '/register', 'title': 'Register Page', 'views': 420, 'percentage': 34},
            {'url': '/cart', 'title': 'Shopping Cart', 'views': 350, 'percentage': 28},
        ]
        
        # Simulated recent activities
        recent_activities = [
            {'username': 'testuser', 'action': 'Added book to cart', 'timestamp': datetime.now(), 'icon': 'shopping-cart'},
            {'username': 'admin', 'action': 'Updated book information', 'timestamp': datetime.now() - timedelta(minutes=15), 'icon': 'edit'},
            {'username': 'newuser1', 'action': 'Registered new account', 'timestamp': datetime.now() - timedelta(minutes=30), 'icon': 'user-plus'},
            {'username': 'customer2', 'action': 'Placed an order', 'timestamp': datetime.now() - timedelta(hours=1), 'icon': 'check-circle'},
            {'username': 'reader3', 'action': 'Browsed fiction category', 'timestamp': datetime.now() - timedelta(hours=2), 'icon': 'book'},
        ]
        
        # Compile analytics data
        analytics = {
            'total_users': total_users,
            'new_users_today': new_users_today,
            'active_users': max(1, int(total_users * 0.6)),  # Simulate 60% active
            'active_percentage': 60,
            'secure_passwords': strong_passwords,
            'password_security_rate': int((strong_passwords / total_users) * 100) if total_users > 0 else 0,
            'page_views_today': traffic_data[-1] if traffic_data else 0,
            'views_increase': random.randint(5, 25),
            
            # User counts
            'customer_count': customer_count,
            'admin_count': admin_count,
            
            # Registration data
            'registrations_this_month': sum(reg_data),
            'registrations_last_month': random.randint(10, 30),
            'registration_labels': registration_labels,
            'registration_data': reg_data,
            
            # Recent users
            'recent_users': recent_users,
            
            # Password security
            'strong_passwords': strong_passwords,
            'medium_passwords': medium_passwords,
            'weak_passwords': weak_passwords,
            'strong_password_percentage': (strong_passwords / total_users * 100) if total_users > 0 else 0,
            'medium_password_percentage': (medium_passwords / total_users * 100) if total_users > 0 else 0,
            'weak_password_percentage': (weak_passwords / total_users * 100) if total_users > 0 else 0,
            
            # Traffic data
            'unique_visitors_today': random.randint(80, 150),
            'bounce_rate': random.randint(25, 45),
            'avg_session_duration': f"{random.randint(2, 8)}m {random.randint(10, 59)}s",
            'traffic_labels': traffic_labels,
            'traffic_data': traffic_data,
            'popular_pages': popular_pages,
            
            # Activity data
            'users_online': random.randint(2, 12),
            'users_last_24h': random.randint(15, 35),
            'users_this_week': random.randint(40, 80),
            'users_this_month': total_users,
            'recent_activities': recent_activities,
        }
        
        cursor.close()
        conn.close()
        
        return render_template('admin_analytics.html', analytics=analytics)
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        print(f"Analytics database error: {e}")
        
        # Provide a complete default analytics structure to prevent template errors
        default_analytics = {
            'total_users': 0,
            'new_users_today': 0,
            'active_users': 0,
            'active_percentage': 0,
            'secure_passwords': 0,
            'password_security_rate': 0,
            'page_views_today': 0,
            'views_increase': 0,
            
            # User counts
            'customer_count': 0,
            'admin_count': 0,
            
            # Registration data
            'registrations_this_month': 0,
            'registrations_last_month': 0,
            'registration_labels': [],
            'registration_data': [],
            
            # Recent users
            'recent_users': [],
            
            # Password security
            'strong_passwords': 0,
            'medium_passwords': 0,
            'weak_passwords': 0,
            'strong_password_percentage': 0,
            'medium_password_percentage': 0,
            'weak_password_percentage': 0,
            
            # Traffic data
            'unique_visitors_today': 0,
            'bounce_rate': 0,
            'avg_session_duration': '0m 0s',
            'traffic_labels': [],
            'traffic_data': [],
            'popular_pages': [],
            
            # Activity data
            'users_online': 0,
            'users_last_24h': 0,
            'users_this_week': 0,
            'users_this_month': 0,
            'recent_activities': [],
        }
        
        return render_template('admin_analytics.html', analytics=default_analytics)
    
    except Exception as e:
        flash(f'Unexpected error: {str(e)}', 'error')
        print(f"Analytics general error: {e}")
        
        # Provide the same default structure for any other errors
        default_analytics = {
            'total_users': 0,
            'new_users_today': 0,
            'active_users': 0,
            'active_percentage': 0,
            'secure_passwords': 0,
            'password_security_rate': 0,
            'page_views_today': 0,
            'views_increase': 0,
            
            # User counts
            'customer_count': 0,
            'admin_count': 0,
            
            # Registration data
            'registrations_this_month': 0,
            'registrations_last_month': 0,
            'registration_labels': [],
            'registration_data': [],
            
            # Recent users
            'recent_users': [],
            
            # Password security
            'strong_passwords': 0,
            'medium_passwords': 0,
            'weak_passwords': 0,
            'strong_password_percentage': 0,
            'medium_password_percentage': 0,
            'weak_password_percentage': 0,
            
            # Traffic data
            'unique_visitors_today': 0,
            'bounce_rate': 0,
            'avg_session_duration': '0m 0s',
            'traffic_labels': [],
            'traffic_data': [],
            'popular_pages': [],
            
            # Activity data
            'users_online': 0,
            'users_last_24h': 0,
            'users_this_week': 0,
            'users_this_month': 0,
            'recent_activities': [],
        }
        
        return render_template('admin_analytics.html', analytics=default_analytics)

# Add category browsing routes
@app.route("/browse")
@app.route("/browse/<category>")
def browse_books(category=None):
    """Browse books by category or show all books"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if category:
            # Browse specific category
            cursor.execute("SELECT * FROM Books WHERE category = %s AND stock > 0", (category,))
            page_title = f"{category} Books"
            page_subtitle = f"Discover amazing {category.lower()} books"
        else:
            # Browse all books
            cursor.execute("SELECT * FROM Books WHERE stock > 0")
            page_title = "Browse All Books"
            page_subtitle = "Explore our complete collection"
            
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('index.html', books=books, 
                             page_title=page_title, page_subtitle=page_subtitle,
                             current_category=category)
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('index.html', books=[], 
                             page_title="Browse Books", page_subtitle="Explore our collection")

@app.route("/bestsellers")
def bestsellers():
    """Show bestselling books (books with high sales)"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get books ordered by popularity (using order count as proxy)
        cursor.execute("""
            SELECT b.*, COALESCE(order_count, 0) as sales
            FROM Books b 
            LEFT JOIN (
                SELECT book_id, COUNT(*) as order_count 
                FROM Order_Items 
                GROUP BY book_id
            ) oi ON b.book_id = oi.book_id
            WHERE b.stock > 0
            ORDER BY sales DESC, b.book_id DESC
            LIMIT 20
        """)
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('index.html', books=books, 
                             page_title="Bestsellers", 
                             page_subtitle="Our most popular books")
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('index.html', books=[], 
                             page_title="Bestsellers", page_subtitle="Our most popular books")

@app.route("/new-arrivals")
def new_arrivals():
    """Show newest books"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Books WHERE stock > 0 ORDER BY created_at DESC LIMIT 20")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('index.html', books=books, 
                             page_title="New Arrivals", 
                             page_subtitle="Recently added books")
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('index.html', books=[], 
                             page_title="New Arrivals", page_subtitle="Recently added books")

@app.route("/free-books")
def free_books():
    """Show free books (price = 0)"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Books WHERE price = 0 AND stock > 0")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('index.html', books=books, 
                             page_title="Free Books", 
                             page_subtitle="Enjoy these books at no cost")
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('index.html', books=[], 
                             page_title="Free Books", page_subtitle="Enjoy these books at no cost")

# Admin user management routes
@app.route("/admin/users")
@admin_required
def admin_users():
    """Admin dashboard for user management"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get all users with their order statistics
        cursor.execute("""
            SELECT u.*, 
                   COALESCE(order_stats.total_orders, 0) as total_orders,
                   COALESCE(order_stats.total_spent, 0) as total_spent,
                   COALESCE(order_stats.books_purchased, 0) as books_purchased
            FROM Users u
            LEFT JOIN (
                SELECT o.user_id,
                       COUNT(DISTINCT o.order_id) as total_orders,
                       SUM(oi.quantity * oi.price) as total_spent,
                       SUM(oi.quantity) as books_purchased
                FROM Orders o
                JOIN Order_Items oi ON o.order_id = oi.order_id
                GROUP BY o.user_id
            ) order_stats ON u.id = order_stats.user_id
            ORDER BY u.created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admin_users.html', users=users)
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('admin_users.html', users=[])

@app.route("/admin/users/<int:user_id>")
@admin_required
def admin_user_detail(user_id):
    """View detailed information about a specific user"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user information
        cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
        
        # Get user's order history
        cursor.execute("""
            SELECT o.*, oi.book_id, oi.quantity, oi.price,
                   b.title, b.author, b.image_url
            FROM Orders o
            JOIN Order_Items oi ON o.order_id = oi.order_id
            JOIN Books b ON oi.book_id = b.book_id
            WHERE o.user_id = %s
            ORDER BY o.order_date DESC
        """, (user_id,))
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin_user_detail.html', user=user, orders=orders)
        
    except mysql.connector.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return redirect(url_for('admin_users'))

@app.route("/search")
def search():
    """Search for books by title, author, or category"""
    query = request.args.get('q', '').strip()
    
    if not query:
        flash('Please enter a search term.', 'error')
        return redirect(url_for('home'))
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Search in title, author, category, and description
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM Books 
            WHERE (title LIKE %s OR author LIKE %s OR category LIKE %s OR description LIKE %s) 
            AND stock > 0
            ORDER BY 
                CASE 
                    WHEN title LIKE %s THEN 1
                    WHEN author LIKE %s THEN 2
                    WHEN category LIKE %s THEN 3
                    ELSE 4
                END, 
                book_id DESC
        """, (search_pattern, search_pattern, search_pattern, search_pattern, 
              search_pattern, search_pattern, search_pattern))
        
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('index.html', books=books, 
                             page_title=f"Search Results for '{query}'", 
                             page_subtitle=f"Found {len(books)} book(s) matching your search",
                             search_query=query)
        
    except mysql.connector.Error as e:
        flash(f'Search error: {str(e)}', 'error')
        return render_template('index.html', books=[], 
                             page_title=f"Search Results for '{query}'", 
                             page_subtitle="No results found")

# Debug endpoint to test database
@app.route("/debug/db")
@admin_required  
def debug_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Test connection
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        # Check Books table structure
        cursor.execute("DESCRIBE Books")
        columns = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'status': 'success',
            'connection': 'OK',
            'test_query': result,
            'books_columns': columns
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

# Add missing columns to Books table if they don't exist
def ensure_books_table_columns():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if created_at column exists
        cursor.execute("SHOW COLUMNS FROM Books LIKE 'created_at'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Books ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("Added created_at column to Books table")
        
        # Check if updated_at column exists
        cursor.execute("SHOW COLUMNS FROM Books LIKE 'updated_at'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Books ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            print("Added updated_at column to Books table")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"Error updating Books table: {e}")

# Call this function when the app starts
ensure_books_table_columns()

# Add a route to initialize sample data (for debugging)
@app.route("/admin/init-data")
@admin_required
def init_sample_data():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if books exist
        cursor.execute("SELECT COUNT(*) as count FROM Books")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            # Insert sample books
            sample_books = [
                ('The Great Gatsby', 'F. Scott Fitzgerald', 12.99, 50, 'Fiction', 
                 'A classic American novel about the Jazz Age.', 
                 'https://covers.openlibrary.org/b/id/8225261-L.jpg'),
                ('To Kill a Mockingbird', 'Harper Lee', 14.99, 30, 'Fiction',
                 'A gripping tale of racial injustice and childhood innocence.',
                 'https://covers.openlibrary.org/b/id/8231258-L.jpg'),
                ('1984', 'George Orwell', 13.99, 40, 'Science Fiction',
                 'A dystopian social science fiction novel.',
                 'https://covers.openlibrary.org/b/id/8664811-L.jpg'),
                ('Pride and Prejudice', 'Jane Austen', 11.99, 25, 'Romance',
                 'A romantic novel of manners.',
                 'https://covers.openlibrary.org/b/id/8231257-L.jpg'),
                ('The Catcher in the Rye', 'J.D. Salinger', 13.50, 35, 'Fiction',
                 'A controversial coming-of-age story.',
                 'https://covers.openlibrary.org/b/id/8231256-L.jpg'),
                ('Dune', 'Frank Herbert', 16.99, 20, 'Science Fiction',
                 'A science fiction masterpiece about desert planet Arrakis.',
                 'https://covers.openlibrary.org/b/id/8664810-L.jpg'),
            ]
            
            for book_data in sample_books:
                cursor.execute(
                    """INSERT INTO Books (title, author, price, stock, category, description, image_url) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    book_data
                )
            
            conn.commit()
            flash(f'Added {len(sample_books)} sample books to the database!', 'success')
        else:
            flash(f'Database already contains {result["count"]} books.', 'info')
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        flash(f'Error initializing data: {str(e)}', 'error')
        print(f"Init data error: {e}")
    
    return redirect(url_for('admin_books'))

# Helper function to safely convert decimal to float
def safe_float(value):
    """Convert decimal.Decimal or any numeric value to float safely"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

@app.route("/debug/test-db")
def debug_test_db():
    """Debug route to test database connectivity"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Test basic connectivity
        cursor.execute("SELECT VERSION() as version")
        version_info = cursor.fetchone()
        
        # Check Books table
        cursor.execute("SELECT COUNT(*) as count FROM Books")
        book_count = cursor.fetchone()
        
        # Get latest books
        cursor.execute("SELECT book_id, title, author, created_at FROM Books ORDER BY book_id DESC LIMIT 3")
        latest_books = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        debug_info = {
            "status": "success",
            "database_version": version_info['version'],
            "books_count": book_count['count'],
            "latest_books": latest_books
        }
        
        return f"""
        <h2>Database Debug Information</h2>
        <p><strong>Status:</strong> ✅ Connected</p>
        <p><strong>MySQL Version:</strong> {debug_info['database_version']}</p>
        <p><strong>Total Books:</strong> {debug_info['books_count']}</p>
        <h3>Latest Books:</h3>
        <ul>
        {''.join([f"<li>ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, Created: {book['created_at']}</li>" for book in debug_info['latest_books']])}
        </ul>
        <p><a href="/admin/books">Go to Admin Dashboard</a></p>
        """
        
    except Exception as e:
        return f"""
        <h2>Database Debug Information</h2>
        <p><strong>Status:</strong> ❌ Error</p>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><a href="/admin/books">Go to Admin Dashboard</a></p>
        """

@app.route("/update_cart", methods=['POST'])
@login_required
def update_cart():
    """Update quantity of items in cart"""
    book_id = request.form.get('book_id')
    quantity = request.form.get('quantity', type=int)
    
    if not book_id or quantity is None or quantity < 0:
        flash('Invalid cart update request.', 'error')
        return redirect(url_for('cart'))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if quantity == 0:
        # Remove item from cart
        session['cart'].pop(str(book_id), None)
        flash('Item removed from cart.', 'success')
    else:
        # Update quantity
        session['cart'][str(book_id)] = quantity
        flash('Cart updated successfully.', 'success')
    
    return redirect(url_for('cart'))

@app.route("/remove_from_cart", methods=['POST'])
@login_required
def remove_from_cart():
    """Remove item from cart"""
    book_id = request.form.get('book_id')
    
    if not book_id:
        flash('Invalid remove request.', 'error')
        return redirect(url_for('cart'))
    
    if 'cart' in session and str(book_id) in session['cart']:
        del session['cart'][str(book_id)]
        flash('Item removed from cart.', 'success')
    
    return redirect(url_for('cart'))

@app.route("/get_cart_count")
def get_cart_count():
    """Get the number of items in cart (for AJAX requests)"""
    if 'cart' not in session:
        return {'count': 0}
    
    total_items = sum(session['cart'].values())
    return {'count': total_items}

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
