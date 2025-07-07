#!/usr/bin/env python3
"""
Debug script to test database operations
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test database connection"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "template_db")
        )
        print("✅ Database connection successful!")
        
        cursor = conn.cursor(dictionary=True)
        
        # Check if Books table exists
        cursor.execute("SHOW TABLES LIKE 'Books'")
        result = cursor.fetchone()
        if result:
            print("✅ Books table exists!")
            
            # Check Books table structure
            cursor.execute("DESCRIBE Books")
            columns = cursor.fetchall()
            print("\n📋 Books table structure:")
            for col in columns:
                print(f"  - {col['Field']}: {col['Type']}")
            
            # Count existing books
            cursor.execute("SELECT COUNT(*) as count FROM Books")
            count_result = cursor.fetchone()
            print(f"\n📚 Current books in database: {count_result['count']}")
            
            # Show existing books
            cursor.execute("SELECT book_id, title, author, price, stock FROM Books LIMIT 5")
            books = cursor.fetchall()
            if books:
                print("\n📖 Sample books:")
                for book in books:
                    print(f"  - ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}")
            else:
                print("\n📖 No books found in database")
                
        else:
            print("❌ Books table does not exist!")
            
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ General error: {e}")

def test_add_book():
    """Test adding a book manually"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "template_db")
        )
        
        cursor = conn.cursor()
        
        # Test book data
        title = "Test Book Debug"
        author = "Debug Author"
        price = 199.99
        stock = 10
        category = "Fiction"
        description = "This is a test book for debugging"
        image_url = "https://via.placeholder.com/300x400"
        
        insert_query = """
        INSERT INTO Books (title, author, price, stock, category, description, image_url) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (title, author, price, stock, category, description, image_url))
        conn.commit()
        
        book_id = cursor.lastrowid
        print(f"✅ Test book added successfully! Book ID: {book_id}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Error adding test book: {e}")
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    print("🔍 Starting database debug tests...\n")
    test_connection()
    print("\n" + "="*50 + "\n")
    test_add_book()
    print("\n🔍 Debug tests completed!")
