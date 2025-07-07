#!/usr/bin/env python3
"""
PageForge - Quick Deployment Check
Final verification script for production readiness
"""

import os
from dotenv import load_dotenv
import mysql.connector

print("🚀 PageForge - Final Deployment Check")
print("=" * 50)

# Check 1: Environment Variables
print("\n1. Environment Configuration:")
load_dotenv()
required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'FLASK_SECRET_KEY']
env_ok = True

for var in required_vars:
    value = os.getenv(var)
    if value:
        if var in ['DB_PASSWORD', 'FLASK_SECRET_KEY']:
            print(f"   ✅ {var}: [PROTECTED]")
        else:
            print(f"   ✅ {var}: {value}")
    else:
        print(f"   ❌ {var}: Missing")
        env_ok = False

# Check 2: Database Connection
print("\n2. Database Connection:")
try:
    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME')
    }
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    print(f"   ✅ Connected to database: {config['database']}")
    print(f"   ✅ Tables found: {len(tables)}")
    
    # Check admin users
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Admin'")
    admin_count = cursor.fetchone()[0]
    print(f"   ✅ Admin users: {admin_count}")
    
    # Check books
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]
    print(f"   ✅ Books in catalog: {book_count}")
    
    cursor.close()
    cnx.close()
    db_ok = True
    
except Exception as e:
    print(f"   ❌ Database error: {e}")
    db_ok = False

# Check 3: Required Files
print("\n3. Required Files:")
required_files = [
    'app.py', 'database_setup.py', 'requirements.txt', '.env',
    'README.md', 'PROJECT_REPORT.md', 'DEPLOYMENT_GUIDE.md',
    'templates/base.html', 'templates/index.html', 'templates/login.html',
    'static/css/style.css', 'static/js/scripts.js'
]

files_ok = True
for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} - Missing")
        files_ok = False

# Check 4: Security
print("\n4. Security Check:")
secret_key = os.getenv('FLASK_SECRET_KEY')
if secret_key and secret_key != 'supersecretkey123':
    print("   ✅ Production Flask secret key configured")
    security_ok = True
else:
    print("   ⚠️  Default Flask secret key - CHANGE FOR PRODUCTION!")
    security_ok = False

# Final Summary
print("\n" + "=" * 50)
print("📊 DEPLOYMENT READINESS SUMMARY")
print("=" * 50)

checks = [
    ("Environment Variables", env_ok),
    ("Database Connection", db_ok),
    ("Required Files", files_ok),
    ("Security Configuration", security_ok)
]

passed = sum(1 for _, ok in checks if ok)
total = len(checks)

for name, ok in checks:
    status = "✅ PASS" if ok else "❌ FAIL"
    print(f"{name}: {status}")

print(f"\nOverall Score: {passed}/{total} ({(passed/total)*100:.0f}%)")

if passed == total:
    print("\n🎉 PageForge is READY for production deployment!")
    print("   Follow DEPLOYMENT_GUIDE.md for deployment instructions.")
elif passed >= 3:
    print("\n⚠️  PageForge is mostly ready with minor issues.")
    print("   Review failed checks before deployment.")
else:
    print("\n❌ PageForge requires fixes before deployment.")
    print("   Address failed checks and run this script again.")

print("\n📚 Documentation:")
print("   • README.md - Setup and usage instructions")
print("   • PROJECT_REPORT.md - Technical documentation")
print("   • DEPLOYMENT_GUIDE.md - Production deployment guide")

print("\n👨‍💻 Developer: Mahender Banoth (IIT Patna)")
print("   GitHub: @mahenderoffl | LinkedIn: Mahender Creates")
