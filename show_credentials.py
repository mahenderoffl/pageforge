#!/usr/bin/env python3
"""
Display current admin credentials
"""

print("="*60)
print("🔐 PAGEFORGE - CURRENT LOGIN CREDENTIALS")
print("="*60)
print()
print("👑 ADMIN ACCOUNT:")
print("   Username: admin")
print("   Password: PageForge@Admin2024!")
print("   Access: Full admin dashboard")
print()
print("👤 TEST USER ACCOUNT:")
print("   Username: testuser") 
print("   Password: TestUser@Secure2024!")
print("   Access: Customer features")
print()
print("🌐 LOGIN URL: http://127.0.0.1:5000/login")
print()
print("📋 TO START SERVER:")
print("   1. Run: START_PAGEFORGE.bat")
print("   2. Or run: python app.py")
print("   3. Open browser to: http://127.0.0.1:5000")
print()
print("="*60)

# Also try to verify these credentials work
try:
    from werkzeug.security import check_password_hash
    from app import get_connection
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT username, password_hash FROM users WHERE role = 'Admin' LIMIT 1")
    admin = cursor.fetchone()
    
    if admin:
        if check_password_hash(admin['password_hash'], "PageForge@Admin2024!"):
            print("✅ Admin password verified in database!")
        else:
            print("❌ Admin password mismatch - updating now...")
            from werkzeug.security import generate_password_hash
            new_hash = generate_password_hash("PageForge@Admin2024!")
            cursor.execute("UPDATE users SET password_hash = %s WHERE role = 'Admin'", (new_hash,))
            conn.commit()
            print("✅ Admin password updated!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"⚠️  Database check failed: {e}")
    print("Try running: python force_update_admin.py")

print("="*60)
