@echo off
cls
echo.
echo 🚀================================================================🚀
echo                    PageForge Digital Bookstore
echo ==================================================================
echo.
echo 📍 Server will start at: http://127.0.0.1:5000
echo.
echo 🔐 STRONG LOGIN CREDENTIALS:
echo    Admin:     admin / PageForge@Admin2024!
echo    Test User: testuser / TestUser@Secure2024!
echo.
echo 📋 INSTRUCTIONS:
echo    1. Wait for "Running on http://127.0.0.1:5000" message
echo    2. Open your web browser
echo    3. Navigate to: http://127.0.0.1:5000
echo    4. Press Ctrl+C in this window to stop server
echo.
echo ==================================================================
echo 🔄 Starting Flask development server...
echo.

python app.py

echo.
echo 🛑 Server stopped.
echo.
pause
