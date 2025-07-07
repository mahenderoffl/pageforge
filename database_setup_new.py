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

# Hashed passwords for default users - STRONG CREDENTIALS
hashed_admin_password = generate_password_hash("PageForge@Admin2024!")
hashed_user_password = generate_password_hash("TestUser@Secure2024!")

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

def create_database():
    """Create database if it doesn't exist"""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' created successfully!")
        
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"❌ Error creating database: {err}")

def create_tables():
    """Create all tables"""
    try:
        cnx = mysql.connector.connect(database=DB_NAME, **config)
        cursor = cnx.cursor()
        
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creating table {table_name}...", end='')
                cursor.execute(table_description)
                print(" ✅")
            except mysql.connector.Error as err:
                print(f" ❌ Error: {err}")
        
        cursor.close()
        cnx.close()
        print("✅ All tables created successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Error connecting to database: {err}")

def insert_sample_data():
    """Insert sample data including default admin user"""
    try:
        cnx = mysql.connector.connect(database=DB_NAME, **config)
        cursor = cnx.cursor()
        
        # Insert default admin user
        admin_query = """
        INSERT IGNORE INTO Users (username, email, password_hash, role) 
        VALUES (%s, %s, %s, %s)
        """
        admin_data = ('admin', 'admin@pageforge.com', hashed_admin_password, 'Admin')
        cursor.execute(admin_query, admin_data)
        
        # Insert sample customer
        customer_query = """
        INSERT IGNORE INTO Users (username, email, password_hash, role) 
        VALUES (%s, %s, %s, %s)
        """
        customer_data = ('testuser', 'user@pageforge.com', hashed_user_password, 'Customer')
        cursor.execute(customer_query, customer_data)
        
        # Insert sample books
        books_data = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 299.00, 50, 'Fiction', 
             'A classic American novel about the Jazz Age.', 
             'https://covers.openlibrary.org/b/id/8225261-L.jpg', '1925-04-10'),
            ('To Kill a Mockingbird', 'Harper Lee', 349.00, 30, 'Fiction',
             'A gripping tale of racial injustice and childhood innocence.',
             'https://covers.openlibrary.org/b/id/8231258-L.jpg', '1960-07-11'),
            ('1984', 'George Orwell', 325.00, 40, 'Science Fiction',
             'A dystopian social science fiction novel.',
             'https://covers.openlibrary.org/b/id/8664811-L.jpg', '1949-06-08'),
            ('Pride and Prejudice', 'Jane Austen', 275.00, 25, 'Romance',
             'A romantic novel of manners.',
             'https://covers.openlibrary.org/b/id/8231257-L.jpg', '1813-01-28'),
            ('The Catcher in the Rye', 'J.D. Salinger', 315.00, 35, 'Fiction',
             'A controversial coming-of-age story.',
             'https://covers.openlibrary.org/b/id/8231256-L.jpg', '1951-07-16'),
        ]
        
        books_query = """
        INSERT IGNORE INTO Books (title, author, price, stock, category, description, image_url, published_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for book_data in books_data:
            cursor.execute(books_query, book_data)
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        print("✅ Sample data inserted successfully!")
        print("📝 Default admin and test user accounts have been created.")
        print("🔐 Please change default passwords in production environment.")
        
    except mysql.connector.Error as err:
        print(f"❌ Error inserting sample data: {err}")

def main():
    """Main setup function"""
    print("🚀 Setting up PageForge Database...")
    print("=" * 40)
    
    create_database()
    create_tables()
    insert_sample_data()
    
    print("=" * 40)
    print("🎉 Database setup completed!")
    print("🔗 You can now run your Flask application!")

if __name__ == '__main__':
    main()
