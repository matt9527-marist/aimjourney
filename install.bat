@echo off
title Aim Journey Assistant - Installation Script

:: Check for Node.js
echo Checking for Node.js...
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install it from https://nodejs.org and run this script again.
    pause
    exit /b
)

:: Install Node.js dependencies
echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install Node.js dependencies.
    pause
    exit /b
)

:: Check for Python (if applicable)
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install it from https://www.python.org and ensure it is added to PATH.
    pause
    exit /b
)

:: Install Python dependencies (if applicable)
if exist requirements.txt (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install Python dependencies.
        pause
        exit /b
    )
)

echo Installation complete! You can now run launch.bat to start the app.
pause
