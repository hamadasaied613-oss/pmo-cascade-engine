@echo off
title Building PMO CASCADE Executable
echo =============================================
echo  Building PMO CASCADE Sovereign Engine EXE
echo =============================================
echo.

REM Check if dist folder exists and clean it
if exist "%~dp0dist\PMO_CASCADE" rmdir /S /Q "%~dp0dist\PMO_CASCADE"

REM Check if output folder exists
if not exist "%~dp0dist\PMO_CASCADE" mkdir "%~dp0dist\PMO_CASCADE"

echo Step 1: Building executable with PyInstaller...
D:\Work\Python\python.exe -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "PMO_CASCADE_Sovereign_Engine" ^
    --add-data "%~dp0SOVEREIGN.html;." ^
    --add-data "%~dp0SOVEREIGN_SERVER.py;." ^
    --add-data "%~dp0static;static" ^
    --add-data "%~dp0_GATEWAY_TABLES;_GATEWAY_TABLES" ^
    --hidden-import uvicorn ^
    --hidden-import uvicorn.logging ^
    --hidden-import uvicorn.loops ^
    --hidden-import uvicorn.loops.auto ^
    --hidden-import uvicorn.protocols ^
    --hidden-import uvicorn.protocols.http ^
    --hidden-import uvicorn.protocols.http.auto ^
    --hidden-import uvicorn.protocols.websocket ^
    --hidden-import uvicorn.protocols.websocket.auto ^
    --hidden-import fastapi ^
    --hidden-import pydantic ^
    --hidden-import openpyxl ^
    --hidden-import webview ^
    --hidden-import sqlite3 ^
    --hidden-import aiohttp ^
    "%~dp0SOVEREIGN_APP.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Copying data files to dist...
if not exist "%~dp0dist\PMO_CASCADE_Sovereign_Engine\_GATEWAY_TABLES" mkdir "%~dp0dist\PMO_CASCADE_Sovereign_Engine\_GATEWAY_TABLES"
copy "%~dp0_GATEWAY_TABLES\gateway.db" "%~dp0dist\PMO_CASCADE_Sovereign_Engine\_GATEWAY_TABLES\gateway.db" /Y

echo.
echo Step 3: Creating launcher script...
copy "%~dp0LAUNCH_APP.bat" "%~dp0dist\PMO_CASCADE_Sovereign_Engine\LAUNCH_APP.bat" /Y

echo.
echo =============================================
echo  BUILD COMPLETE!
echo  Executable at: dist\PMO_CASCADE_Sovereign_Engine
echo =============================================
echo.
echo  To create a distributable zip:
echo  1. Right-click dist\PMO_CASCADE_Sovereign_Engine folder
echo  2. Send to > Compressed (zipped) folder
echo  3. Upload the zip to Gumroad
echo.
pause
