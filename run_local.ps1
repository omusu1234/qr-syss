# PowerShell script to run the Flask server locally
Write-Host "Setting up environment variables..." -ForegroundColor Green
$env:DATABASE_URL = "postgresql://admin:v3Uti3qu17RvBLrrcrNlXDTVE3S6712u@dpg-d4dcib8gjchc73dsrb8g-a.oregon-postgres.render.com/admin_jxqo"
$env:ENABLE_DB_SYNC = "false"
$env:LOCAL_IP = "10.102.162.145"

Write-Host ""
Write-Host "Starting Flask server on port 5002..." -ForegroundColor Green
Write-Host "Server will be accessible at:" -ForegroundColor Yellow
Write-Host "  - Local: http://localhost:5002" -ForegroundColor Cyan
Write-Host "  - Network: http://10.102.162.145:5002" -ForegroundColor Cyan
Write-Host ""
Write-Host "QR codes will use: http://10.102.162.145:5002" -ForegroundColor Magenta
Write-Host ""

python app.py

