@echo off
title Aim Journey Assistant - Installation Script

:: Function to set PYTHON_CMD based on availability of python or python3
echo Checking for Python installation...
where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python3"
    ) else (
        echo Neither Python nor Python3 is installed. Please install Python from https://www.python.org and add it to PATH.
        pause
        exit /b
    )
)

:: Check Python version
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to verify Python installation. Ensure Python is correctly installed and added to PATH.
    pause
    exit /b
)

:: Install pip if not available
echo Checking for pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed. Installing pip...
    %PYTHON_CMD% -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Failed to install pip. Ensure Python is correctly installed.
        pause
        exit /b
    )
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

:: Install SpaCy
echo Installing SpaCy...
%PYTHON_CMD% -m pip install spacy
if %errorlevel% neq 0 (
    echo Failed to install SpaCy. Check your Python and pip setup.
    pause
    exit /b
)

:: Install SpaCy Model
echo Downloading SpaCy English model...
%PYTHON_CMD% -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo Failed to download the SpaCy model. Ensure you have an internet connection.
    pause
    exit /b
)

:: Install openpyxl
echo Installing openpyxl...
pip install openpyxl --upgrade
if %errorlevel% neq 0 (
    echo Failed to install openpyxl. Check your Python and pip setup.
    pause
    exit /b
)

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

echo Installation complete! You can now run launch.bat to start the app.
pause