#!/usr/bin/env python3
"""
Add created_at column to Users table
"""

from app import get_connection
import mysql.connector

def add_created_at_column():
    """Add created_at column to Users table if it doesn't exist"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("🔧 Checking Users table structure...")
        
        # Check if created_at column exists
        cursor.execute("SHOW COLUMNS FROM Users LIKE 'created_at'")
        has_created_at = cursor.fetchone() is not None
        
        if not has_created_at:
            print("📅 Adding created_at column to Users table...")
            
            # Add created_at column with default timestamp
            cursor.execute("""
                ALTER TABLE Users 
                ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)
            
            # Update existing users with current timestamp
            cursor.execute("""
                UPDATE Users 
                SET created_at = CURRENT_TIMESTAMP 
                WHERE created_at IS NULL
            """)
            
            conn.commit()
            print("✅ Successfully added created_at column to Users table")
        else:
            print("✅ created_at column already exists")
        
        cursor.close()
        conn.close()
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error updating Users table: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PageForge - Users Table Update")
    print("="*40)
    
    if add_created_at_column():
        print("\n🎉 Users table updated successfully!")
        print("The analytics dashboard should now work properly.")
    else:
        print("\n❌ Failed to update Users table.")
        print("Please check the database connection and try again.")
