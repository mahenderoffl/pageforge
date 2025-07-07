#!/usr/bin/env python3
"""
Check Users table structure to see if it has a created_at column
"""

from app import get_connection

def check_users_table():
    """Check Users table structure"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("DESCRIBE Users")
        columns = cursor.fetchall()
        
        print("📋 Users Table Structure:")
        print("-" * 40)
        for i, column in enumerate(columns, 1):
            print(f"{i:2}. {column[0]:15} - {column[1]}")
        
        # Check if created_at column exists
        column_names = [col[0] for col in columns]
        if 'created_at' in column_names:
            print("\n✅ created_at column exists")
            
            # Check sample data
            cursor.execute("SELECT username, created_at FROM Users LIMIT 3")
            sample_users = cursor.fetchall()
            
            if sample_users:
                print("👥 Sample users with creation dates:")
                for user in sample_users:
                    print(f"   {user[0]}: {user[1]}")
            else:
                print("👥 No users in database")
                
        else:
            print("\n❌ created_at column missing!")
            print("Adding created_at column...")
            cursor.execute("ALTER TABLE Users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
            print("✅ created_at column added with default timestamp")
            
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking Users table: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking Users table structure...")
    print("=" * 50)
    check_users_table()
    print("=" * 50)
    print("✅ Done!")
