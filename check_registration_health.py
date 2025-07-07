#!/usr/bin/env python3
"""
Quick health check for registration functionality
"""

def check_registration():
    try:
        import mysql.connector
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Test database connection
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "template_db")
        )
        
        cursor = conn.cursor()
        
        # Check if Users table exists and has correct structure
        cursor.execute("SHOW TABLES LIKE 'Users'")
        if not cursor.fetchone():
            print("❌ Users table does not exist")
            return False
        
        # Check table structure
        cursor.execute("DESCRIBE Users")
        columns = cursor.fetchall()
        print("✓ Users table structure:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Check current user count
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        print(f"✓ Current users in database: {user_count}")
        
        cursor.close()
        conn.close()
        
        print("✓ Database connection and Users table are working")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    check_registration()
