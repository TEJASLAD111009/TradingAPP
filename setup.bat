@echo off
REM Trading App - Quick Setup Script for Windows
REM This script automates the setup process for the Trading App

echo.
echo ===============================================
echo  Trading App - Setup & Installation
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation... OK
python --version

echo.
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

echo.
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/4] Launching Streamlit application...
echo.
echo ===============================================
echo  Setup Complete! Starting application...
echo ===============================================
echo.
echo Demo Credentials:
echo  Username: demo | Password: demo123
echo  Username: trader | Password: trader123
echo  Username: user | Password: password123
echo.
echo App will open in your browser at: http://localhost:8501
echo.

streamlit run main.py

pause
