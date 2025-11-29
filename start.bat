@echo off
echo Starting Location Tracker Server...
start /B python server.py
timeout /t 2 /nobreak >nul
echo Opening browser...
start http://localhost:3000
echo.
echo Server is running!
echo Press Ctrl+C to stop the server
echo.
pause
