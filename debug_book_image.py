#!/usr/bin/env python3
"""
Debug script to test book updates including image URLs
"""

from app import get_connection

def test_book_update():
    """Test updating a book with image URL"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get the first book
        cursor.execute("SELECT * FROM Books LIMIT 1")
        book = cursor.fetchone()
        
        if book:
            print("Original book data:")
            print(f"ID: {book['book_id']}")
            print(f"Title: {book['title']}")
            print(f"Image URL: {book.get('image_url', 'None')}")
            print()
            
            # Test updating with a new image URL
            test_image_url = "https://via.placeholder.com/300x400/007bff/ffffff?text=Test+Book"
            
            cursor.execute(
                """UPDATE Books SET image_url = %s WHERE book_id = %s""",
                (test_image_url, book['book_id'])
            )
            conn.commit()
            print(f"Updated image URL to: {test_image_url}")
            
            # Verify the update
            cursor.execute("SELECT * FROM Books WHERE book_id = %s", (book['book_id'],))
            updated_book = cursor.fetchone()
            
            print("\nAfter update:")
            print(f"Image URL: {updated_book.get('image_url', 'None')}")
            
            if updated_book['image_url'] == test_image_url:
                print("✅ Image URL update successful!")
            else:
                print("❌ Image URL update failed!")
                
        else:
            print("No books found in database")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

def check_books_table_structure():
    """Check if the Books table has the image_url column"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DESCRIBE Books")
        columns = cursor.fetchall()
        
        print("Books table structure:")
        for column in columns:
            print(f"  {column[0]} - {column[1]}")
            
        # Check if image_url column exists
        column_names = [col[0] for col in columns]
        if 'image_url' in column_names:
            print("\n✅ image_url column exists")
        else:
            print("\n❌ image_url column missing!")
            print("Adding image_url column...")
            cursor.execute("ALTER TABLE Books ADD COLUMN image_url TEXT")
            conn.commit()
            print("✅ image_url column added")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error checking table structure: {e}")

if __name__ == "__main__":
    print("🔍 Debugging Book Image URL Updates")
    print("="*50)
    
    print("1. Checking table structure...")
    check_books_table_structure()
    
    print("\n2. Testing book update...")
    test_book_update()
