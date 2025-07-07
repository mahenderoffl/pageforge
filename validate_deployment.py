#!/usr/bin/env python3
"""
PageForge - Final Deployment Validation Script
Developed by Mahender Banoth (IIT Patna)

This script performs comprehensive validation checks to ensure
PageForge is ready for production deployment.
"""

import os
import sys
import mysql.connector
from dotenv import load_dotenv

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_environment():
    """Check environment configuration"""
    print_header("Environment Configuration Check")
    
    # Load environment variables
    load_dotenv()
    
    required_vars = [
        'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'FLASK_SECRET_KEY'
    ]
    
    all_vars_present = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'DB_PASSWORD':
                print_success(f"{var}: [PROTECTED]")
            elif var == 'FLASK_SECRET_KEY':
                if value == 'supersecretkey123':
                    print_error(f"{var}: Using default key - CHANGE FOR PRODUCTION!")
                    all_vars_present = False
                else:
                    print_success(f"{var}: [SECURE KEY SET]")
            else:
                print_success(f"{var}: {value}")
        else:
            print_error(f"{var}: Not set")
            all_vars_present = False
    
    return all_vars_present

def check_file_structure():
    """Check required files exist"""
    print_header("File Structure Validation")
    
    required_files = [
        'app.py',
        'database_setup.py',
        'requirements.txt',
        '.env',
        'README.md',
        'PROJECT_REPORT.md',
        'DEPLOYMENT_GUIDE.md',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/admin_books.html',
        'templates/admin_users.html',
        'static/css/style.css',
        'static/js/scripts.js'
    ]
    
    all_files_present = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - Missing")
            all_files_present = False
    
    return all_files_present

def check_database_connection():
    """Check database connection and schema"""
    print_header("Database Connection & Schema Check")
    
    try:
        load_dotenv()
        config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME')
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        print_success("Database connection established")
        
        # Check required tables
        required_tables = ['Users', 'Books', 'Cart', 'Orders', 'OrderItems']
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        tables_ok = True
        for table in required_tables:
            if table in existing_tables:
                print_success(f"Table '{table}' exists")
            else:
                print_error(f"Table '{table}' missing")
                tables_ok = False
        
        # Check for admin user
        cursor.execute("SELECT COUNT(*) FROM Users WHERE role = 'Admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count > 0:
            print_success(f"Admin users found: {admin_count}")
        else:
            print_warning("No admin users found - run database_setup.py")
        
        # Check for sample books
        cursor.execute("SELECT COUNT(*) FROM Books")
        book_count = cursor.fetchone()[0]
        
        if book_count > 0:
            print_success(f"Books in database: {book_count}")
        else:
            print_warning("No books found - run database_setup.py")
        
        cursor.close()
        cnx.close()
        
        return tables_ok and admin_count > 0
        
    except mysql.connector.Error as err:
        print_error(f"Database error: {err}")
        return False
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False

def check_python_dependencies():
    """Check Python dependencies"""
    print_header("Python Dependencies Check")
    
    try:
        import flask
        print_success(f"Flask: {flask.__version__}")
    except ImportError:
        print_error("Flask not installed")
        return False
    
    import importlib.util
    if importlib.util.find_spec("mysql.connector") is not None:
        print_success("mysql-connector-python: Available")
    else:
        print_error("mysql-connector-python not installed")
        return False

    if importlib.util.find_spec("dotenv") is not None:
        print_success("python-dotenv: Available")
    else:
        print_error("python-dotenv not installed")
        return False
    
    if importlib.util.find_spec("werkzeug.security") is not None:
        print_success("Werkzeug: Available")
    else:
        print_error("Werkzeug not installed")
        return False
    
    return True

def check_security_measures():
    """Check security implementation"""
    print_header("Security Measures Validation")
    
    security_score = 0
    
    # Check if .env file exists and is not tracked
    if os.path.exists('.env'):
        print_success(".env file exists")
        security_score += 1
    else:
        print_error(".env file missing")
    
    # Check .gitignore exists and contains .env
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print_success(".env is gitignored")
                security_score += 1
            else:
                print_warning(".env should be in .gitignore")
    else:
        print_warning(".gitignore file missing")
    
    # Check for hardcoded passwords in app.py
    with open('app.py', 'r') as f:
        app_content = f.read()
        if 'password' in app_content.lower() and ('PageForge@Admin2024!' in app_content or 'TestUser@Secure2024!' in app_content):
            print_error("Hardcoded strong passwords found in app.py - move to database setup only")
        else:
            print_success("No hardcoded passwords in app.py")
            security_score += 1
    
    # Check Flask secret key
    load_dotenv()
    secret_key = os.getenv('FLASK_SECRET_KEY')
    if secret_key and secret_key != 'supersecretkey123':
        print_success("Production Flask secret key configured")
        security_score += 1
    else:
        print_error("Default Flask secret key detected - CHANGE FOR PRODUCTION!")
    
    return security_score >= 3

def check_ui_completeness():
    """Check UI/UX completeness"""
    print_header("UI/UX Completeness Check")
    
    # Check CSS file exists and has content
    css_file = 'static/css/style.css'
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            css_content = f.read()
            if len(css_content) > 1000:  # Basic check for substantial CSS
                print_success("CSS file has substantial styling")
            else:
                print_warning("CSS file seems minimal")
    else:
        print_error("CSS file missing")
    
    # Check JS file exists
    js_file = 'static/js/scripts.js'
    if os.path.exists(js_file):
        with open(js_file, 'r') as f:
            js_content = f.read()
            if 'modal' in js_content.lower():
                print_success("JavaScript includes modal functionality")
            else:
                print_warning("JavaScript may be missing modal functionality")
    else:
        print_error("JavaScript file missing")
    
    # Check template files have proper structure
    template_files = ['base.html', 'index.html', 'login.html', 'register.html']
    templates_ok = True
    
    for template in template_files:
        template_path = f'templates/{template}'
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                content = f.read()
                if '{% extends' in content or '<!DOCTYPE html>' in content:
                    print_success(f"{template} has proper structure")
                else:
                    print_warning(f"{template} may have structural issues")
        else:
            print_error(f"{template} missing")
            templates_ok = False
    
    return templates_ok

def run_full_validation():
    """Run complete validation suite"""
    print_header("PageForge - Final Deployment Validation")
    print_info("Developed by Mahender Banoth (IIT Patna)")
    print_info("Checking production readiness...")
    
    checks = [
        ("Environment Configuration", check_environment),
        ("File Structure", check_file_structure),
        ("Python Dependencies", check_python_dependencies),
        ("Database Connection", check_database_connection),
        ("Security Measures", check_security_measures),
        ("UI/UX Completeness", check_ui_completeness)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_function in checks:
        try:
            if check_function():
                passed_checks += 1
        except Exception as e:
            print_error(f"Error in {check_name}: {e}")
    
    # Final summary
    print_header("Validation Summary")
    
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"Checks Passed: {passed_checks}/{total_checks}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 100:
        print_success("🎉 PageForge is READY for production deployment!")
        print_info("All validation checks passed successfully.")
        print_info("Proceed with deployment using DEPLOYMENT_GUIDE.md")
    elif success_rate >= 80:
        print_warning("⚠️  PageForge is mostly ready with minor issues.")
        print_info("Review failed checks before deployment.")
    else:
        print_error("❌ PageForge requires fixes before deployment.")
        print_info("Address failed checks and run validation again.")
    
    print(f"\n{Colors.BLUE}{Colors.BOLD}Next Steps:{Colors.END}")
    print("1. Review DEPLOYMENT_GUIDE.md for deployment instructions")
    print("2. Update production environment variables")
    print("3. Run database_setup.py on production server")
    print("4. Configure web server (Nginx + Gunicorn)")
    print("5. Set up SSL certificate")
    print("6. Perform final testing")
    
    return success_rate >= 80

if __name__ == "__main__":
    try:
        success = run_full_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_error("\n\nValidation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        sys.exit(1)
