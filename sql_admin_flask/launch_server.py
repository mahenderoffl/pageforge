#!/usr/bin/env python3
"""
PageForge - Development Server Launcher
Auto-starts the Flask development server with proper configuration
"""

def print_banner():
    """Print startup banner"""
    print("🚀" + "="*58 + "🚀")
    print("    PageForge Digital Bookstore - Development Server")
    print("="*60)
    print("📍 Server URL: http://127.0.0.1:5000")
    print("🔐 Admin Login: admin / PageForge@Admin2024!")
    print("👤 User Login: testuser / TestUser@Secure2024!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("="*60)

def check_prerequisites():
    """Check if everything is ready"""
    try:
        # Test database connection
        from app import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        print("✅ Database connection verified")
        
        # Test Flask app
        from app import app
        print("✅ Flask application loaded")
        print(f"✅ Routes configured: {len(app.url_map._rules)}")
        
        return True
    except Exception as e:
        print(f"❌ Prerequisites check failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check .env file configuration")
        print("3. Run: python database_setup.py")
        return False

def start_server():
    """Start the Flask development server"""
    print_banner()
    
    if not check_prerequisites():
        input("\nPress Enter to exit...")
        return
    
    print("\n🔄 Starting Flask development server...")
    print("⏳ Please wait for 'Running on http://127.0.0.1:5000' message...")
    print()
    
    try:
        # Import and run the app
        from app import app
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Thanks for using PageForge!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if port 5000 is available")
        print("2. Verify database is running")
        print("3. Check error logs above")
    finally:
        print("\n" + "="*60)
        input("Press Enter to exit...")

if __name__ == "__main__":
    start_server()
