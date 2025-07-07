#!/usr/bin/env python3
"""
Test script to check registration functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_registration():
    try:
        import app
        
        # Create test client
        client = app.app.test_client()
        app.app.config['TESTING'] = True
        
        print("Testing registration functionality...")
        
        # Test GET request to register page
        response = client.get('/register')
        print(f'✓ GET /register status: {response.status_code}')
        
        if response.status_code != 200:
            print(f"❌ Registration page not loading properly")
            return False
        
        # Test POST request with sample data
        test_data = {
            'username': 'testuser123',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'confirm_password': 'TestPass123',
            'terms': 'on'
        }
        
        response = client.post('/register', data=test_data, follow_redirects=False)
        print(f'✓ POST /register status: {response.status_code}')
        
        if response.status_code == 302:
            print(f"✓ Registration redirected to: {response.location}")
        elif response.status_code == 200:
            print("❌ Registration returned to same page (likely error)")
            # Check response content for error messages
            response_text = response.get_data(as_text=True)
            if 'error' in response_text.lower():
                print("Found error in response")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

if __name__ == "__main__":
    test_registration()
