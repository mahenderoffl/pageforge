#!/usr/bin/env python3
"""
Test analytics dashboard functionality directly
"""

from app import app, admin_analytics
import sys

def test_analytics():
    """Test the analytics function directly"""
    print("🧪 Testing Analytics Dashboard")
    print("=" * 50)
    
    try:
        with app.app_context():
            # Mock the session for admin access
            with app.test_request_context():
                from flask import session
                session['user_id'] = 1  # Admin user
                session['role'] = 'Admin'
                
                # Call the analytics function
                result = admin_analytics()
                
                if hasattr(result, 'status_code'):
                    print(f"✅ Analytics route returned successfully (status: {result.status_code})")
                else:
                    print("✅ Analytics route returned template response")
                    
                print("✅ No template errors - analytics dashboard should work!")
                
    except Exception as e:
        print(f"❌ Error testing analytics: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True

if __name__ == "__main__":
    success = test_analytics()
    print("=" * 50)
    if success:
        print("✅ Analytics dashboard test passed!")
    else:
        print("❌ Analytics dashboard test failed!")
        sys.exit(1)
