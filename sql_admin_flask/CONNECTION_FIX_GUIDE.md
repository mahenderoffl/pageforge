# 🔧 PageForge Server Connection Fix Guide

## ❌ **PROBLEM**: "Unable to connect to 127.0.0.1:5000"

This error means the Flask server is **not running**. Here are the solutions:

---

## 🚀 **SOLUTION 1: Easy Start (RECOMMENDED)**

### **Step 1: Double-Click Start File**
1. Find `START_PAGEFORGE.bat` in your project folder
2. **Double-click it**
3. Wait for "Running on http://127.0.0.1:5000"
4. Open browser and go to: **http://127.0.0.1:5000**

---

## 💻 **SOLUTION 2: Manual Command Line**

### **Step 1: Open Command Prompt**
- Press `Win + R`, type `cmd`, press Enter

### **Step 2: Navigate to Project**
```cmd
cd "c:\Users\user\Desktop\sql_admin_flask"
```

### **Step 3: Start Server**
```cmd
python app.py
```

### **Step 4: Wait for Success Message**
Look for:
```
* Debug mode: on
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
```

### **Step 5: Open Browser**
Go to: **http://127.0.0.1:5000**

---

## 🔍 **SOLUTION 3: Advanced Launcher**

```cmd
cd "c:\Users\user\Desktop\sql_admin_flask"
python launch_server.py
```

---

## 🛠️ **TROUBLESHOOTING**

### **❌ Error: "python" not recognized**
**Solution**: Add Python to PATH or use full path:
```cmd
C:\Python311\python.exe app.py
```

### **❌ Error: Port 5000 already in use**
**Solution**: Kill existing processes:
```cmd
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### **❌ Error: Database connection failed**
**Solution**: Check MySQL is running:
```cmd
python quick_check.py
```

### **❌ Error: Module not found**
**Solution**: Install dependencies:
```cmd
pip install -r requirements.txt
```

### **❌ Browser shows "This site can't be reached"**
**Causes**:
- Server not started yet
- Wrong URL (use `http://` not `https://`)
- Firewall blocking connection

**Solution**: 
1. Check server is running (look for "Running on..." message)
2. Use exact URL: **http://127.0.0.1:5000**
3. Allow Python through Windows Firewall

---

## ✅ **VERIFICATION CHECKLIST**

Before starting, verify:
- [ ] You're in the correct directory: `c:\Users\user\Desktop\sql_admin_flask`
- [ ] MySQL service is running
- [ ] All Python packages installed: `pip list`
- [ ] Database is set up: `python quick_check.py`
- [ ] No other application using port 5000

---

## 🎯 **WHAT YOU SHOULD SEE**

### **In Terminal/Command Window:**
```
* Debug mode: on
* Running on http://127.0.0.1:5000
* Restarting with stat
* Debugger is active!
* Debugger PIN: xxx-xxx-xxx
```

### **In Browser (http://127.0.0.1:5000):**
- 🎨 Beautiful dark theme homepage
- 📚 Book catalog with sample books
- 🔐 Login/Register buttons in navigation
- 📱 Responsive design

---

## 🔑 **LOGIN CREDENTIALS**

Once the server is running:

**Admin Dashboard Access:**
- Username: `admin`
- Password: `PageForge@Admin2024!`
- URL: http://127.0.0.1:5000/login

**Test User Access:**
- Username: `testuser`
- Password: `TestUser@Secure2024!`
- URL: http://127.0.0.1:5000/login

---

## 🚨 **STILL NOT WORKING?**

### **Quick Diagnosis:**
```cmd
cd "c:\Users\user\Desktop\sql_admin_flask"
python -c "from app import app; print('App OK')"
python -c "from app import get_connection; get_connection(); print('DB OK')"
```

### **Check System Status:**
```cmd
python quick_check.py
```

### **Restart Everything:**
1. Close all command windows
2. Restart MySQL service
3. Run `START_PAGEFORGE.bat` again

---

## 📞 **Emergency Commands**

### **Force Kill Python Processes:**
```cmd
taskkill /IM python.exe /F
```

### **Check What's Using Port 5000:**
```cmd
netstat -ano | findstr :5000
```

### **Reset Database:**
```cmd
python database_setup.py
```

---

## 🎉 **SUCCESS INDICATORS**

You'll know it's working when:
- ✅ Command window shows "Running on http://127.0.0.1:5000"
- ✅ Browser loads the PageForge homepage
- ✅ You can see books displayed
- ✅ Login/Register buttons work
- ✅ Navigation is responsive

---

**🎯 Bottom Line: The server MUST be running for the website to work. Follow Solution 1 for the easiest start!**

---

*Last Updated: December 2024*  
*Status: Ready for Launch 🚀*
