@echo off
title PMO CASCADE Sovereign Engine
echo =============================================
echo  PMO CASCADE Sovereign Engine v2.0
echo =============================================
echo.

:: Kill any existing instances
taskkill /F /IM python.exe /FI "WINDOWTITLE eq SOVEREIGN*" >nul 2>&1

:: Check if server is already running on port 9000
netstat -ano | findstr ":9000" | findstr "LISTENING" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  Starting server on port 9000...
    start /B "" D:\Work\Python\python.exe "%~dp0SOVEREIGN_SERVER.py"
    timeout /t 3 /nobreak >nul
    echo  Server started!
) else (
    echo  Server already running on port 9000
)

echo.
echo  Opening in browser...
start http://localhost:9000

echo.
echo  App is running at http://localhost:9000
echo  Close this window or press Ctrl+C to stop.
echo.
pause
