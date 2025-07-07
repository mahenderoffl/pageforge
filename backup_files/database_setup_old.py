import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'March2@2004'),
    'host': os.getenv('DB_HOST', 'localhost')
}

DB_NAME = os.getenv('DB_NAME', 'template_db')

# Hashed passwords for default users
hashed_admin_password = generate_password_hash("admin123")
hashed_user_password = generate_password_hash("user123")

TABLES = {}

# Users table for authentication
TABLES['Users'] = (
    """
    CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM('Admin', 'Customer') DEFAULT 'Customer',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
)

TABLES['Books'] = (
    """
    CREATE TABLE IF NOT EXISTS Books (
        book_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255),
        price DECIMAL(10,2),
        stock INT DEFAULT 0,
        category VARCHAR(100),
        description TEXT,
        image_url VARCHAR(500),
        published_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
)

TABLES['Orders'] = (
    """
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
        shipping_address TEXT,
        phone VARCHAR(20),
        payment_method VARCHAR(50),
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
    )
    """
)

TABLES['Order_Items'] = (
    """
    CREATE TABLE IF NOT EXISTS Order_Items (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        book_id INT NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
    )
    """
)

# Legacy tables for compatibility
TABLES['Admins'] = (
    """
    CREATE TABLE IF NOT EXISTS Admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM('Manager', 'Staff') DEFAULT 'Staff'
    )
    """
)

TABLES['Customers'] = (
    """
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(20),
        address TEXT
    )
    """
)
    )
    """
)

TABLES['Orders'] = (
    """
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(10,2),
        status ENUM('Pending', 'Completed', 'Cancelled'),
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    )
    """
)

TABLES['Order_Items'] = (
    """
    CREATE TABLE IF NOT EXISTS Order_Items (
        order_item_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        book_id INT,
        quantity INT,
        subtotal DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (book_id) REFERENCES Books(book_id)
    )
    """
)

TABLES['Templates'] = (
    """
    CREATE TABLE IF NOT EXISTS Templates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        code VARCHAR(100) NOT NULL UNIQUE,
        type VARCHAR(100) NOT NULL,
        status ENUM('Active', 'Inactive') DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
)

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.database = DB_NAME
    print(f"✅ Database `{DB_NAME}` selected/created.")

    for table_name, table_sql in TABLES.items():
        cursor.execute(table_sql)
        print(f"✅ Table `{table_name}` created.")

    # Sample Data Insertion
    cursor.execute("""
        INSERT INTO Templates (name, code, type, status)
        VALUES 
        ('Welcome Email', 'WEL001', 'Email', 'Active'),
        ('Newsletter', 'NEWS001', 'Email', 'Active'),
        ('Invoice', 'INV001', 'Document', 'Active')
    """)

    cursor.execute("""
        INSERT INTO Books (title, author, price, stock, category, published_date)
        VALUES
        ('The Great Gatsby', 'F. Scott Fitzgerald', 10.99, 50, 'Fiction', '1925-04-10'),
        ('1984', 'George Orwell', 8.99, 40, 'Dystopian', '1949-06-08'),
        ('To Kill a Mockingbird', 'Harper Lee', 12.50, 30, 'Classic', '1960-07-11'),
        ('The Catcher in the Rye', 'J.D. Salinger', 9.99, 20, 'Novel', '1951-07-16'),
        ('Moby Dick', 'Herman Melville', 15.75, 25, 'Adventure', '1851-10-18')
    """)

    cursor.execute("""
        INSERT INTO Admins (username, password_hash, role)
        VALUES ('admin1', %s, 'Manager')
    """, (hashed_admin_password,))

    conn.commit()
    print("✅ Sample data inserted successfully.")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
finally:
    cursor.close()
    conn.close()
