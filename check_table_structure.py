#!/usr/bin/env python3
"""
Quick test to verify Books table structure and image URL functionality
"""

from app import get_connection

def check_books_table():
    """Check Books table structure and image URL column"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("DESCRIBE Books")
        columns = cursor.fetchall()
        
        print("📋 Books Table Structure:")
        print("-" * 40)
        for i, column in enumerate(columns, 1):
            print(f"{i:2}. {column[0]:15} - {column[1]}")
        
        # Check if image_url column exists
        column_names = [col[0] for col in columns]
        if 'image_url' in column_names:
            print("\n✅ image_url column exists")
            
            # Get a sample book with image URL
            cursor.execute("SELECT book_id, title, image_url FROM Books WHERE image_url IS NOT NULL AND image_url != '' LIMIT 1")
            book_with_image = cursor.fetchone()
            
            if book_with_image:
                print("📚 Sample book with image:")
                print(f"   ID: {book_with_image[0]}")
                print(f"   Title: {book_with_image[1]}")
                print(f"   Image URL: {book_with_image[2]}")
            else:
                print("📚 No books have image URLs set")
                
        else:
            print("\n❌ image_url column missing!")
            print("Adding image_url column...")
            cursor.execute("ALTER TABLE Books ADD COLUMN image_url TEXT")
            conn.commit()
            print("✅ image_url column added")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_simple_update():
    """Test a simple image URL update"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get first book
        cursor.execute("SELECT * FROM Books LIMIT 1")
        book = cursor.fetchone()
        
        if book:
            book_id = book['book_id']
            test_url = "https://example.com/test-image.jpg"
            
            print(f"\n🔧 Testing update on book ID {book_id}")
            print(f"   Current image_url: {book.get('image_url', 'None')}")
            
            # Update image URL
            cursor.execute("UPDATE Books SET image_url = %s WHERE book_id = %s", (test_url, book_id))
            conn.commit()
            
            # Verify update
            cursor.execute("SELECT image_url FROM Books WHERE book_id = %s", (book_id,))
            result = cursor.fetchone()
            
            print(f"   New image_url: {result['image_url']}")
            
            if result['image_url'] == test_url:
                print("   ✅ Update successful!")
            else:
                print("   ❌ Update failed!")
                
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during test update: {e}")

if __name__ == "__main__":
    print("🔍 PageForge Books Table Diagnostics")
    print("=" * 50)
    
    check_books_table()
    test_simple_update()
    
    print("\n" + "=" * 50)
    print("💡 If the table structure looks correct,")
    print("   the issue might be in the web form.")
    print("   Check browser console for JavaScript errors.")
