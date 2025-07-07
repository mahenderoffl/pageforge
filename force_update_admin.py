#!/usr/bin/env python3
"""
Force update admin password
"""

from werkzeug.security import generate_password_hash
from app import get_connection

def update_admin_password():
    """Force update admin password"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Generate new hash for the strong password
        new_password = "PageForge@Admin2024!"
        password_hash = generate_password_hash(new_password)
        
        # Update admin password
        cursor.execute("UPDATE users SET password_hash = %s WHERE role = 'Admin'", (password_hash,))
        affected = cursor.rowcount
        conn.commit()
        
        print(f"Updated {affected} admin user(s)")
        print(f"New password: {new_password}")
        
        # Verify the update
        cursor.execute("SELECT username, role FROM users WHERE role = 'Admin'")
        admins = cursor.fetchall()
        for admin in admins:
            print(f"Admin user: {admin[0]} ({admin[1]})")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Admin password updated successfully!")
        print("You can now login with:")
        print("Username: admin")
        print(f"Password: {new_password}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_admin_password()
