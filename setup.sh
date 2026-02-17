#!/bin/bash
# Trading App - Quick Setup Script for macOS/Linux
# This script automates the setup process for the Trading App

echo ""
echo "==============================================="
echo "  Trading App - Setup & Installation"
echo "==============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Checking Python installation... OK"
python3 --version

echo ""
echo "[2/4] Creating virtual environment..."

if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully"
fi

echo ""
echo "[3/4] Installing dependencies..."

source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[4/4] Launching Streamlit application..."
echo ""
echo "==============================================="
echo "  Setup Complete! Starting application..."
echo "==============================================="
echo ""
echo "Demo Credentials:"
echo "  Username: demo | Password: demo123"
echo "  Username: trader | Password: trader123"
echo "  Username: user | Password: password123"
echo ""
echo "App will open in your browser at: http://localhost:8501"
echo ""

streamlit run main.py
