#!/usr/bin/env python3
"""
Simple Flask App Runner
Run this file to start your Flask application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("✅ Flask app imported successfully!")
    print("🚀 Starting Flask development server...")
    print("📍 Your app will be available at: http://127.0.0.1:5000")
    print("🔄 Press Ctrl+C to stop the server")
    app.run(host='127.0.0.1', port=5000, debug=True)
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure Flask is installed: pip install Flask")
except Exception as e:
    print(f"❌ Error starting Flask app: {e}")
    print("💡 Check your app.py file for syntax errors")
