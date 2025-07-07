#!/usr/bin/env python3
"""
Test script to debug the book addition issue
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "template_db")
    )

def test_database_connection():
    """Test basic database connectivity"""
    print("🔍 Testing database connection...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ Connected to MySQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_books_table():
    """Check if Books table exists and its structure"""
    print("\n📋 Checking Books table...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'Books'")
        if not cursor.fetchone():
            print("❌ Books table does not exist!")
            cursor.close()
            conn.close()
            return False
        
        print("✅ Books table exists!")
        
        # Show table structure
        cursor.execute("DESCRIBE Books")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} {'(NULL)' if col[2] == 'YES' else '(NOT NULL)'}")
        
        # Count existing books
        cursor.execute("SELECT COUNT(*) FROM Books")
        count = cursor.fetchone()[0]
        print(f"\n📚 Current books count: {count}")
        
        if count > 0:
            print("\nExisting books:")
            cursor.execute("SELECT book_id, title, author, created_at FROM Books ORDER BY book_id DESC LIMIT 5")
            books = cursor.fetchall()
            for book in books:
                print(f"  - ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Created: {book[3]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking Books table: {e}")
        return False

def add_test_book():
    """Add a test book to verify insertion works"""
    print("\n➕ Adding test book...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Test book data
        title = "Debug Test Book"
        author = "Test Author"
        price = 299.99
        stock = 5
        category = "Fiction"
        description = "This is a test book to debug the addition issue"
        image_url = "https://via.placeholder.com/300x400/007bff/ffffff?text=Test+Book"
        
        # Insert the book
        insert_query = """
        INSERT INTO Books (title, author, price, stock, category, description, image_url) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (title, author, price, stock, category, description, image_url))
        conn.commit()
        
        book_id = cursor.lastrowid
        print(f"✅ Test book added successfully! Book ID: {book_id}")
        
        # Verify the book was added
        cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book_id,))
        book = cursor.fetchone()
        if book:
            print(f"✅ Verification successful: Book '{book[1]}' found in database")
        else:
            print("❌ Verification failed: Book not found after insertion")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding test book: {e}")
        return False

def main():
    print("🚀 Starting book addition debug tests...\n")
    
    # Test 1: Database connection
    if not test_database_connection():
        print("❌ Database connection failed. Cannot proceed.")
        return
    
    # Test 2: Books table check
    if not check_books_table():
        print("❌ Books table check failed. Cannot proceed.")
        return
    
    # Test 3: Add test book
    if add_test_book():
        print("\n✅ All tests passed! Book addition should work.")
    else:
        print("\n❌ Test book addition failed!")
    
    print("\n🏁 Debug tests completed!")

if __name__ == "__main__":
    main()
