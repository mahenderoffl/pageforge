#!/usr/bin/env python3
"""
Test script to debug and fix the analytics route
"""

def test_analytics_route():
    print("🔍 Testing Analytics Route")
    print("=" * 40)
    
    try:
        import app
        from flask import Flask
        
        # Create test client
        client = app.app.test_client()
        app.app.config['TESTING'] = True
        
        print("✅ App imported successfully")
        
        # Test the analytics route directly
        with app.app.test_request_context():
            try:
                # Simulate admin session
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                    sess['username'] = 'admin'
                    sess['role'] = 'Admin'
                
                print("✅ Test session created")
                
                # Test GET request to analytics
                response = client.get('/admin/analytics')
                print(f"📊 Analytics route status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Analytics route working properly!")
                    print("🎉 All analytics data should be available now")
                elif response.status_code == 302:
                    print("⚠️  Redirected (likely authentication issue)")
                else:
                    print(f"❌ Unexpected status code: {response.status_code}")
                    print("Response data:", response.get_data(as_text=True)[:500])
                
                return response.status_code == 200
                
            except Exception as route_error:
                print(f"❌ Route test error: {route_error}")
                return False
        
    except Exception as e:
        print(f"❌ Import/setup error: {e}")
        return False

def check_database_tables():
    print("\n🗄️  Checking Database Tables")
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
        
        # Check critical tables
        tables_to_check = ['Users', 'Books', 'Orders']
        
        for table in tables_to_check:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            if cursor.fetchone():
                print(f"✅ {table} table exists")
            else:
                print(f"❌ {table} table missing")
        
        # Check Users table structure
        cursor.execute("DESCRIBE Users")
        columns = [col[0] for col in cursor.fetchall()]
        
        print(f"\n📋 Users table columns: {', '.join(columns)}")
        
        if 'created_at' in columns:
            print("✅ created_at column exists")
        else:
            print("⚠️  created_at column missing (using fallback)")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Analytics Diagnostics")
    print("=" * 50)
    
    db_ok = check_database_tables()
    route_ok = test_analytics_route()
    
    print(f"\n📋 Results:")
    print(f"Database: {'✅ OK' if db_ok else '❌ Issues'}")
    print(f"Analytics Route: {'✅ OK' if route_ok else '❌ Issues'}")
    
    if db_ok and route_ok:
        print("\n🎉 Analytics should be working now!")
        print("💡 Try accessing: http://127.0.0.1:5000/admin/analytics")
    else:
        print("\n🔧 Issues detected - but default fallback should prevent errors")
        print("💡 Analytics page will show with default values")
