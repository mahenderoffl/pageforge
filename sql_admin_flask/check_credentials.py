#!/usr/bin/env python3
"""
PageForge - Login Credentials Checker
Check current admin credentials and test login
"""

from werkzeug.security import check_password_hash
from app import get_connection

def check_credentials():
    """Check and display current login credentials"""
    
    print("🔐 PageForge - Current Login Credentials")
    print("="*50)
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get admin user
        cursor.execute("SELECT * FROM users WHERE role = 'Admin' LIMIT 1")
        admin = cursor.fetchone()
        
        # Get test user
        cursor.execute("SELECT * FROM users WHERE role = 'Customer' AND username = 'testuser' LIMIT 1")
        test_user = cursor.fetchone()
        
        if admin:
            print(f"\n👑 ADMIN ACCOUNT:")
            print(f"   Username: {admin['username']}")
            print(f"   Email: {admin['email']}")
            print(f"   Role: {admin['role']}")
            
            # Test the strong password
            strong_password = "PageForge@Admin2024!"
            if check_password_hash(admin['password_hash'], strong_password):
                print(f"   Password: {strong_password} ✅")
                print("   Status: ✅ WORKING")
            else:
                print("   Password: ❌ Strong password not working")
                # Test old password
                if check_password_hash(admin['password_hash'], "admin123"):
                    print("   Password: admin123 (OLD - still active)")
                    print("   Status: ⚠️  OLD CREDENTIALS")
                else:
                    print("   Status: ❌ PASSWORD UNKNOWN")
        else:
            print("❌ No admin user found!")
        
        if test_user:
            print(f"\n👤 TEST USER ACCOUNT:")
            print(f"   Username: {test_user['username']}")
            print(f"   Email: {test_user['email']}")
            print(f"   Role: {test_user['role']}")
            
            # Test the strong password
            strong_password = "TestUser@Secure2024!"
            if check_password_hash(test_user['password_hash'], strong_password):
                print(f"   Password: {strong_password} ✅")
                print("   Status: ✅ WORKING")
            else:
                print("   Password: ❌ Strong password not working")
                # Test old password
                if check_password_hash(test_user['password_hash'], "user123"):
                    print("   Password: user123 (OLD - still active)")
                    print("   Status: ⚠️  OLD CREDENTIALS")
                else:
                    print("   Status: ❌ PASSWORD UNKNOWN")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("🌐 LOGIN URL: http://127.0.0.1:5000/login")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error checking credentials: {e}")

if __name__ == "__main__":
    check_credentials()
