@echo off
echo Setting up environment variables...
set DATABASE_URL=postgresql://admin:v3Uti3qu17RvBLrrcrNlXDTVE3S6712u@dpg-d4dcib8gjchc73dsrb8g-a.oregon-postgres.render.com/admin_jxqo
set ENABLE_DB_SYNC=false
set LOCAL_IP=10.104.227.145
echo.
echo Starting Flask server on port 5002...
echo Server will be accessible at:
echo   - Local: http://localhost:5002
echo   - Network: http://10.104.227.145:5002
echo.
echo QR codes will use: http://10.104.227.145:5002
echo.
python app.py
pause

