import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'March2@2004'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'template_db')
}

def migrate_database():
    """Add missing columns to existing tables"""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        # Check if description column exists in Books table
        cursor.execute("SHOW COLUMNS FROM Books LIKE 'description'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding description column to Books table...")
            cursor.execute("ALTER TABLE Books ADD COLUMN description TEXT AFTER category")
            print("✅ Description column added successfully!")
        else:
            print("✅ Description column already exists!")
        
        # Check if image_url column exists in Books table
        cursor.execute("SHOW COLUMNS FROM Books LIKE 'image_url'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding image_url column to Books table...")
            cursor.execute("ALTER TABLE Books ADD COLUMN image_url VARCHAR(500) AFTER description")
            print("✅ Image_url column added successfully!")
        else:
            print("✅ Image_url column already exists!")
        
        # Check if published_date column exists in Books table
        cursor.execute("SHOW COLUMNS FROM Books LIKE 'published_date'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding published_date column to Books table...")
            cursor.execute("ALTER TABLE Books ADD COLUMN published_date DATE AFTER image_url")
            print("✅ Published_date column added successfully!")
        else:
            print("✅ Published_date column already exists!")
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        print("🎉 Database migration completed successfully!")
        
    except mysql.connector.Error as err:
        print(f"❌ Migration error: {err}")

if __name__ == '__main__':
    print("🔄 Running database migration...")
    migrate_database()
