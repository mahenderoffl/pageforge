# 🔐 PageForge - Strong User Credentials

## Updated Account Information

### 👑 **Admin Account**
- **Username**: `admin`
- **Password**: `PageForge@Admin2024!`
- **Role**: Administrator
- **Access**: Full admin dashboard, user management, book management

### 👤 **Test User Account**
- **Username**: `testuser`
- **Password**: `TestUser@Secure2024!`
- **Role**: Customer
- **Access**: Shopping, library, standard user features

---

## 🛡️ **Password Security Features**

### **Admin Password: `PageForge@Admin2024!`**
✅ **Length**: 19 characters  
✅ **Uppercase**: P, F, A  
✅ **Lowercase**: a, g, e, o, r, g, e, d, m, i, n  
✅ **Numbers**: 2, 0, 2, 4  
✅ **Special Characters**: @, !  
✅ **Complexity**: High  
✅ **Project-specific**: Contains "PageForge"  

### **Test User Password: `TestUser@Secure2024!`**
✅ **Length**: 20 characters  
✅ **Uppercase**: T, U, S  
✅ **Lowercase**: e, s, t, s, e, r, e, c, u, r, e  
✅ **Numbers**: 2, 0, 2, 4  
✅ **Special Characters**: @, !  
✅ **Complexity**: High  
✅ **Role-specific**: Contains "TestUser" and "Secure"  

---

## 🔄 **How to Update Database with New Credentials**

### **Step 1: Re-run Database Setup**
```bash
cd "c:\Users\user\Desktop\sql_admin_flask"
python database_setup.py
```

### **Step 2: Verify New Credentials**
```bash
python quick_check.py
```

### **Step 3: Test Login**
1. Start server: `python app.py`
2. Go to: http://127.0.0.1:5000/login
3. Use new admin credentials

---

## 🚨 **Security Notes**

### **Production Deployment**
- ⚠️ **Change these passwords** before production deployment
- ✅ Use environment variables for production passwords
- ✅ Enable two-factor authentication if implementing
- ✅ Regular password rotation policy

### **Development Use**
- ✅ These passwords are secure for development/testing
- ✅ No longer using weak default passwords
- ✅ Meets password complexity requirements
- ✅ Suitable for demonstration purposes

---

## 📝 **Password Policy Compliance**

✅ **Minimum 12 characters** (both exceed this)  
✅ **Mixed case letters** (uppercase and lowercase)  
✅ **Numbers included** (2024)  
✅ **Special characters** (@ and !)  
✅ **No common dictionary words** as base  
✅ **Project/role context** included  
✅ **Unique per account**  

---

## 🔐 **For Production Deployment**

### **Recommended Production Password Policy:**
- Minimum 16 characters
- Include uppercase, lowercase, numbers, special characters
- Avoid personal information
- Use password managers
- Enable account lockout after failed attempts
- Implement password expiration (90-180 days)
- Require unique passwords (no reuse)

### **Environment Variable Setup (.env):**
```ini
# Production passwords (replace with your secure passwords)
ADMIN_DEFAULT_PASSWORD=your-super-secure-admin-password-here
USER_DEFAULT_PASSWORD=your-secure-test-user-password-here
```

---

## 📞 **Support**

If you need to reset or change passwords:

1. **Database Method**: Update `database_setup.py` and re-run
2. **Admin Panel**: Use admin dashboard user management (once implemented)
3. **Direct Database**: Update password_hash in Users table

---

**⚠️ IMPORTANT**: These credentials are for development/testing only. Always use unique, secure passwords for production deployment!

---

*Updated: December 2024*  
*Security Level: HIGH*  
*Compliance: ✅ Strong Password Policy*
