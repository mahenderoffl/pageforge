# PageForge - Current Login Credentials

## Admin Account
- **Username:** `admin`
- **Password:** `PageForge@Admin2024!`
- **Role:** Admin
- **Access:** Full admin dashboard, user management, book management

## Test User Account  
- **Username:** `testuser`
- **Password:** `TestUser@Secure2024!`
- **Role:** Customer
- **Access:** Browse books, shopping cart, order history

## Login Instructions

1. **Start the server:**
   ```
   python app.py
   ```

2. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/login
   ```

3. **Use the credentials above to login**

## If Login Still Fails

If you're still unable to login with these credentials, run this command to force update the admin password:

```
python force_update_admin.py
```

This will ensure the admin password is set to `PageForge@Admin2024!` in the database.

## Password Security Features

- All passwords are hashed using Werkzeug's PBKDF2 algorithm
- Strong password requirements enforced
- No plain text passwords stored in database
- Session-based authentication with secure cookies

---
**Developer:** Mahender Banoth (IIT Patna)  
**Project:** PageForge Digital Bookstore
