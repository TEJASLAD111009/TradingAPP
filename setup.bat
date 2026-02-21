@echo off
REM Trading App - Cross-platform Setup Script for Windows
REM This script automates the setup process for the Trading App

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  Trading App - Cross-platform Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo Error: Python is not installed or not in PATH
        echo Please install Python 3.8+ from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo [1/5] Checking Python installation... OK
%PYTHON_CMD% --version

echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [4/5] Installing dependencies...
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [5/5] Creating .env file from template...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo .env file created. Please update it with your API keys.
    )
) else (
    echo .env file already exists
)

echo.
echo ===============================================
echo  Setup Complete! Starting application...
echo ===============================================
echo.
echo Demo Credentials:
echo  Username: demo ^| Password: demo123
echo  Username: trader ^| Password: trader123
echo  Username: user ^| Password: password123
echo.
echo App will open in your browser at: http://localhost:8501
echo.

streamlit run main.py

pause
