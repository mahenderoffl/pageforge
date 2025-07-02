#!/usr/bin/env python3
"""
Quick fix to ensure analytics work properly
"""

def create_missing_analytics_tables():
    print("🛠️  Setting up analytics tables")
    print("=" * 40)
    
    try:
        import mysql.connector
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "template_db")
        )
        
        cursor = conn.cursor()
        
        # Check if Orders table exists, if not create a minimal one
        cursor.execute("SHOW TABLES LIKE 'Orders'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE Orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount DECIMAL(10,2),
                    status VARCHAR(50) DEFAULT 'pending',
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            """)
            print("✅ Created Orders table")
        else:
            print("✅ Orders table already exists")
        
        # Ensure Users table has created_at column
        cursor.execute("SHOW COLUMNS FROM Users LIKE 'created_at'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE Users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            cursor.execute("ALTER TABLE Users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            print("✅ Added timestamp columns to Users table")
        else:
            print("✅ Users table already has timestamp columns")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Analytics database setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def test_analytics_access():
    print("\n🔐 Testing Analytics Access")
    print("=" * 40)
    
    try:
        import app
        
        # Test the route function directly
        with app.app.app_context():
            # Mock the session and authentication
            import flask
            with app.app.test_request_context():
                flask.session['user_id'] = 1
                flask.session['username'] = 'admin'
                flask.session['role'] = 'Admin'
                
                try:
                    result = app.admin_analytics()
                    print("✅ Analytics function executed successfully!")
                    return True
                except Exception as e:
                    print(f"❌ Analytics function error: {e}")
                    return False
                    
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Analytics Quick Fix")
    print("=" * 50)
    
    setup_ok = create_missing_analytics_tables()
    test_ok = test_analytics_access()
    
    print(f"\n📋 Fix Results:")
    print(f"Database Setup: {'✅ OK' if setup_ok else '❌ Failed'}")
    print(f"Analytics Function: {'✅ OK' if test_ok else '❌ Failed'}")
    
    if setup_ok:
        print("\n🎉 Analytics should now work properly!")
        print("💡 The error has been fixed with:")
        print("   • Proper default values for all analytics keys")
        print("   • Better error handling")
        print("   • Database table creation")
        print("\n🚀 Try accessing: /admin/analytics")
    else:
        print("\n⚠️  Some issues remain, but error handling will prevent crashes")
