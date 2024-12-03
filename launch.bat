@echo off
title Aim Journey Assistant - Launcher

:: Start the server
echo Starting the server...
start cmd /k "node server.js"
if %errorlevel% neq 0 (
    echo Failed to start the server. Ensure server.js exists and Node.js is installed.
    pause
    exit /b
)

:: Launch the client
echo Launching the client...
npm run start
if %errorlevel% neq 0 (
    echo Failed to start the client. Ensure all dependencies are installed correctly.
    pause
    exit /b
)

pause