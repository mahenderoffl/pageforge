Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    PageForge Digital Bookstore" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Starting Flask development server..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Server will be available at: http://127.0.0.1:5000" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Please wait for 'Running on http://127.0.0.1:5000' message..." -ForegroundColor Yellow
Write-Host "🌐 Then open your browser and visit the URL above" -ForegroundColor Yellow
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python app.py
} catch {
    Write-Host ""
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're in the correct directory" -ForegroundColor White
    Write-Host "2. Check if MySQL is running" -ForegroundColor White
    Write-Host "3. Verify .env file exists with database credentials" -ForegroundColor White
    Write-Host "4. Run: python database_setup.py" -ForegroundColor White
}

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
