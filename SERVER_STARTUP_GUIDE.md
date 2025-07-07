# 🚀 How to Start PageForge Server

## Quick Start Instructions

### Method 1: Using Python directly
1. Open Command Prompt or PowerShell
2. Navigate to your project folder:
   ```cmd
   cd "c:\Users\user\Desktop\sql_admin_flask"
   ```
3. Start the server:
   ```cmd
   python app.py
   ```
4. Open your browser and go to: **http://127.0.0.1:5000**

### Method 2: Using the startup script
1. Double-click `start_server.bat` in the project folder
2. Wait for the server to start
3. Open your browser and go to: **http://127.0.0.1:5000**

### Method 3: Using the Python startup script
1. Open Command Prompt in the project folder
2. Run:
   ```cmd
   python start_pageforge.py
   ```
3. Open your browser and go to: **http://127.0.0.1:5000**

---

## Troubleshooting

### ❌ "Unable to connect" Error
**Causes:**
- Server is not running
- Wrong URL/port
- Firewall blocking connection

**Solutions:**
1. **Check if server is running**: Look for output like:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

2. **Verify the correct URL**: Make sure you're using `http://127.0.0.1:5000` (not https)

3. **Check Windows Firewall**: Allow Python through Windows Defender Firewall

### ❌ Database Connection Errors
**Solutions:**
1. Make sure MySQL is running
2. Check your `.env` file has correct database credentials
3. Run database setup:
   ```cmd
   python database_setup.py
   ```

### ❌ Module Import Errors
**Solutions:**
1. Install required packages:
   ```cmd
   pip install -r requirements.txt
   ```

### ❌ Port Already in Use
**Solutions:**
1. Kill any existing Python processes
2. Change port in `app.py` (line 944):
   ```python
   app.run(debug=True, host='127.0.0.1', port=5001)  # Changed to 5001
   ```

---

## Expected Server Output

When the server starts successfully, you should see:
```
* Debug mode: on
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
* Debugger PIN: xxx-xxx-xxx
```

---

## Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `PageForge@Admin2024!`

**Test User Account:**
- Username: `testuser`
- Password: `TestUser@Secure2024!`

⚠️ **IMPORTANT**: Change these passwords in production!

---

## Browser Testing

1. **Home Page**: http://127.0.0.1:5000
2. **Login**: http://127.0.0.1:5000/login
3. **Register**: http://127.0.0.1:5000/register
4. **Admin Dashboard**: http://127.0.0.1:5000/admin/books (after admin login)

---

## Common URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:5000 |
| Login | http://127.0.0.1:5000/login |
| Register | http://127.0.0.1:5000/register |
| Cart | http://127.0.0.1:5000/cart |
| My Library | http://127.0.0.1:5000/my-library |
| Admin Books | http://127.0.0.1:5000/admin/books |
| Admin Users | http://127.0.0.1:5000/admin/users |
| Browse Fiction | http://127.0.0.1:5000/browse/Fiction |
| Search | http://127.0.0.1:5000/search?q=python |

---

## Server Management

### To Stop the Server:
- Press `Ctrl + C` in the terminal/command prompt

### To Restart the Server:
1. Stop the server (Ctrl + C)
2. Run the start command again

### To View Logs:
- Server logs appear in the terminal where you started the server
- Look for any error messages in red

---

## Need Help?

If you're still having issues:

1. **Check Python version**: Run `python --version` (should be 3.7+)
2. **Check MySQL service**: Make sure MySQL is running
3. **Verify dependencies**: Run `pip list` to see installed packages
4. **Test database**: Run `python quick_check.py` for diagnosis

**Contact**: For technical support, refer to the project documentation or GitHub repository.

---

*PageForge Digital Bookstore - Ready for your reading journey! 📚*
