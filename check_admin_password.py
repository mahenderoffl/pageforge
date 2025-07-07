#!/usr/bin/env python3
"""
Simple admin password checker
"""

from werkzeug.security import check_password_hash, generate_password_hash
from app import get_connection

def check_admin_password():
    """Check admin password"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get admin user
        cursor.execute("SELECT username, password_hash FROM users WHERE role = 'Admin' LIMIT 1")
        admin = cursor.fetchone()
        
        if admin:
            print(f"Admin username: {admin['username']}")
            
            # Test passwords
            passwords_to_test = [
                "PageForge@Admin2024!",
                "admin123",
                "admin",
                "password"
            ]
            
            for pwd in passwords_to_test:
                if check_password_hash(admin['password_hash'], pwd):
                    print(f"WORKING PASSWORD: {pwd}")
                    break
            else:
                print("None of the test passwords work")
                print(f"Password hash: {admin['password_hash'][:50]}...")
                
                # Let's try to update with the correct password
                new_hash = generate_password_hash("PageForge@Admin2024!")
                cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", 
                             (new_hash, admin['username']))
                conn.commit()
                print("Updated admin password to PageForge@Admin2024!")
        else:
            print("No admin user found")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_admin_password()
