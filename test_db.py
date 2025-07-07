#!/usr/bin/env python3
"""
Test script to check database connectivity and book data
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def test_database():
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'template_db')
        )
        
        cursor = conn.cursor(dictionary=True)
        
        print("✅ Database connection successful!")
        
        # Check if Books table exists
        cursor.execute("SHOW TABLES LIKE 'Books'")
        if cursor.fetchone():
            print("✅ Books table exists")
            
            # Check book count
            cursor.execute("SELECT COUNT(*) as count FROM Books")
            result = cursor.fetchone()
            print(f"📚 Total books in database: {result['count']}")
            
            # Show sample books
            cursor.execute("SELECT book_id, title, author, price, stock FROM Books ORDER BY book_id DESC LIMIT 5")
            books = cursor.fetchall()
            
            if books:
                print("\n📖 Recent books:")
                for book in books:
                    print(f"  {book['book_id']}: {book['title']} by {book['author']} - ${book['price']} (Stock: {book['stock']})")
            else:
                print("❌ No books found in database")
                
        else:
            print("❌ Books table does not exist")
        
        # Check Users table
        cursor.execute("SHOW TABLES LIKE 'Users'")
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) as count FROM Users")
            result = cursor.fetchone()
            print(f"👥 Total users in database: {result['count']}")
            
            cursor.execute("SELECT username, role FROM Users")
            users = cursor.fetchall()
            print("Users:")
            for user in users:
                print(f"  {user['username']} ({user['role']})")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ General error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🔍 Testing PageForge Database...")
    print("=" * 40)
    
    if test_database():
        print("\n✅ Database test completed successfully!")
    else:
        print("\n❌ Database test failed!")
        print("\n💡 Try running: python database_setup.py")
