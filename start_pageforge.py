#!/usr/bin/env python3
"""
PageForge Server Startup Script
Run this to start the PageForge digital bookstore server
"""

import sys
from app import app

def start_server():
    """Start the PageForge Flask development server"""
    
    print("🚀 Starting PageForge Digital Bookstore Server...")
    print("=" * 60)
    print("Server will start on: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        # Check database connection first
        from app import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        print("✅ Database connection verified")
        
        # Start the Flask development server
        print("🌐 Starting Flask server...")
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check your .env file configuration")
        print("3. Run 'python database_setup.py' if needed")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
