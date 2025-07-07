#!/usr/bin/env python3
"""
Test the enhanced registration functionality
"""

def test_registration_improvements():
    print("🧪 Testing Enhanced Registration System")
    print("=" * 50)
    
    # Test 1: Check if registration page loads
    try:
        import app
        client = app.app.test_client()
        app.app.config['TESTING'] = True
        
        response = client.get('/register')
        print(f"✅ Registration page loads: {response.status_code == 200}")
        
        # Test 2: Test password validation
        invalid_passwords = [
            ('short', 'too short'),
            ('nouppercase123', 'no uppercase'),
            ('NOLOWERCASE123', 'no lowercase'),
            ('NoNumbers', 'no numbers'),
            ('', 'empty password')
        ]
        
        print("\n🔐 Testing Password Validation:")
        for password, description in invalid_passwords:
            test_data = {
                'username': 'testuser',
                'email': 'test@test.com',
                'password': password,
                'confirm_password': password,
                'terms': 'on'
            }
            
            response = client.post('/register', data=test_data, follow_redirects=False)
            success = response.status_code == 200  # Should stay on page with error
            print(f"  ❌ {description}: {'Correctly rejected' if success else 'Unexpectedly accepted'}")
        
        # Test 3: Test valid registration
        print("\n✅ Testing Valid Registration:")
        valid_data = {
            'username': 'ValidUser123',
            'email': 'valid@example.com',
            'password': 'StrongPass123',
            'confirm_password': 'StrongPass123',
            'terms': 'on'
        }
        
        response = client.post('/register', data=valid_data, follow_redirects=False)
        redirect_success = response.status_code == 302
        print(f"  ✅ Valid registration: {'Accepted' if redirect_success else 'Rejected'}")
        
        print("\n🎉 Registration system test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def check_template_features():
    print("\n🎨 Checking Template Features:")
    print("=" * 30)
    
    try:
        with open('templates/register.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        features = [
            ('password-toggle', 'Password visibility toggle'),
            ('password-requirements', 'Password requirements display'),
            ('password-strength', 'Password strength indicator'),
            ('password-match', 'Password match validation'),
            ('togglePassword', 'JavaScript toggle function'),
            ('calculatePasswordStrength', 'Password strength calculator'),
            ('fas fa-eye', 'Eye icon for visibility')
        ]
        
        for feature, description in features:
            if feature in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} - Missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Template check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PageForge Registration System Test")
    print("=" * 50)
    
    test_registration_improvements()
    check_template_features()
    
    print("\n📝 Enhanced Features Added:")
    print("  • Real-time password strength indicator")
    print("  • Enhanced password visibility toggle")
    print("  • Improved form validation")
    print("  • Better error handling")
    print("  • Case-insensitive duplicate checking")
    print("  • Enhanced username format validation")
    print("  • Loading state on form submission")
    print("  • Comprehensive client-side validation")
    
    print("\n🎯 Usage Instructions:")
    print("1. Start the server: python app.py")
    print("2. Go to: http://127.0.0.1:5000/register")
    print("3. Try the enhanced password features!")
    print("4. Test the real-time validation!")
