#!/usr/bin/env python3
"""
Simple Flask app test
"""
import sys

print("Starting Flask app test...")
print(f"Python version: {sys.version}")

try:
    from app import app
    print("✅ App imported successfully!")
    
    # Test if we can access routes
    with app.test_client() as client:
        print("✅ Test client created!")
        
        # Test admin_books route
        try:
            response = client.get('/admin/books')
            print(f"✅ Admin books route accessible (status: {response.status_code})")
        except Exception as e:
            print(f"❌ Error accessing admin books route: {e}")
            
except Exception as e:
    print(f"❌ Error importing app: {e}")
    import traceback
    traceback.print_exc()

print("Test completed!")
