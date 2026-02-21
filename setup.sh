#!/bin/bash
# Trading App - Cross-platform Setup Script for Linux, macOS, and Windows (Git Bash/WSL)

set -e  # Exit on error

echo ""
echo "==============================================="
echo "  Trading App - Cross-platform Setup"
echo "==============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python 3.8+ is not installed"
    echo "Please install Python from: https://www.python.org/downloads/"
    exit 1
fi

# Determine which Python command to use
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "[1/5] Checking Python installation... OK"
$PYTHON_CMD --version

echo ""
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    $PYTHON_CMD -m venv venv
    echo "Virtual environment created successfully"
fi

echo ""
echo "[3/5] Activating virtual environment..."
# Handle both Unix and Windows paths
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Warning: Could not find activate script"
fi

echo ""
echo "[4/5] Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "[5/5] Creating .env file from template..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ".env file created. Please update it with your API keys."
    fi
else
    echo ".env file already exists"
fi

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

# Launch Streamlit
streamlit run main.py
