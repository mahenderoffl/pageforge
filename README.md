# PageForge - Premium Digital Bookstore

A modern Flask-based e-commerce platform for digital books with premium UI design, admin management, and user authentication.

## 🚀 Features

- **Premium UI Design**: Modern, responsive interface with gradient designs
- **User Authentication**: Secure registration and login system
- **Admin Dashboard**: Complete book management system
- **Shopping Cart**: Full e-commerce functionality with Indian Rupee (₹) pricing
- **Book Library**: Personal library for purchased books
- **Real-time Validation**: Client-side and server-side validation
- **Mobile Responsive**: Works perfectly on all devices
- **GST Integration**: 18% GST calculation for Indian market

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL Server
- Git (optional)

### Installation

1. **Clone or download the project**
   ```bash
   cd sql_admin_flask
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**
   - Update database connection settings in `db.py`
   - Ensure MySQL server is running

4. **Initialize Database**
   ```bash
   python database_setup.py
   ```
   This will create all necessary tables and sample data.

5. **Run the Application**
   ```bash
   python app.py
   ```
   
6. **Access the Application**
   - Open your browser and go to `http://localhost:5000`
   - The application will be running with sample books and user accounts

## 🔐 Security Notes

- **Production Deployment**: Change all default passwords before deploying to production
- **Environment Variables**: Use environment variables for sensitive configuration
- **Database Security**: Ensure proper database security measures are in place

## 📂 Project Structure

```
sql_admin_flask/
├── app.py                 # Main Flask application
├── db.py                  # Database configuration
├── database_setup.py      # Database initialization
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── admin_books.html  # Admin dashboard
│   ├── book_form.html    # Add/Edit book form
│   └── ...
└── static/               # Static assets (if any)
```

## 👨‍💻 Developer

**Mahender Banoth (IIT Patna)**
- Instagram: [@mahender_hustles](https://www.instagram.com/mahender_hustles/)
- LinkedIn: [Mahender Hustles](https://www.linkedin.com/in/mahender-hustles/)
- GitHub: [mahenderoffl](https://github.com/mahenderoffl)

*"I am an AI enthusiast studying at IIT Patna, driven by curiosity and a vision to shape the tech-driven future."*

## 📄 License

This project is for educational and demonstration purposes.

---

**Note**: This is a demo application. Please implement additional security measures for production use.
