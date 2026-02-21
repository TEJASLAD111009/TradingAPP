# Cross-Platform Deployment Guide

This guide helps you deploy the Trading App on Windows, Linux (Render), macOS, and other platforms.

## Key Changes Made for Cross-Platform Compatibility

### 1. **Environment Variables (.env file)**
- All sensitive data and configuration moved to environment variables
- Use `.env.example` as template
- Never commit `.env` file to version control

### 2. **Path Handling**
- Replaced hardcoded Windows paths (`d:\trading\data\`) with dynamic path resolution
- Used `os.path.join()` for cross-platform path compatibility
- Models now use relative paths from project root

### 3. **Python Imports**
- Added `pathlib.Path` for modern path handling
- Updated setup scripts to handle both `python` and `python3` commands
- Windows and Unix shell script differences handled

### 4. **API Configuration**
- API keys now loaded from environment variables
- Supports different API keys for different environments
- Better security with environment-based config

---

## Platform-Specific Setup Instructions

### **Windows**
```powershell
# Run the setup script
.\setup.bat

# Or manually:
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API keys
streamlit run main.py
```

### **Linux (including Render.com)**
```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
streamlit run main.py
```

### **macOS**
```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
streamlit run main.py
```

---

## Deploying to Render.com (Linux)

### 1. **Create a `render.yaml` file**
```yaml
services:
  - type: web
    name: trading-app
    env: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: STREAMLIT_SERVER_PORT
        value: 10000
      - key: STREAMLIT_SERVER_ADDRESS
        value: 0.0.0.0
```

### 2. **Environment Variables on Render**
Add in Render Dashboard:
```
ALPHA_VANTAGE_API_KEY=your_api_key
BASE_CURRENCY=USD
CONVERSION_CURRENCY=INR
INITIAL_WALLET_BALANCE=1000.0
YFINANCE_ENABLED=true
```

### 3. **Deploy**
```bash
git push origin main
# Render will automatically deploy
```

---

## Deploying to AWS/DigitalOcean/Heroku

### **Docker Support**
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t trading-app .
docker run -p 8501:8501 --env-file .env trading-app
```

---

## Key Environment Variables

```env
# Currency
BASE_CURRENCY=USD
CONVERSION_CURRENCY=INR

# Wallet
INITIAL_WALLET_BALANCE=1000.0

# API
ALPHA_VANTAGE_API_KEY=your_key_here
YFINANCE_ENABLED=true

# Streamlit
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## Database File Locations

All data is stored in `data/` directory:
- `data/users.json` - User credentials
- `data/wallets.json` - User wallets
- `data/portfolios.json` - User portfolios

These are created automatically on first run.

---

## Troubleshooting

### **Module not found errors**
```bash
# Ensure you're in virtual environment
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### **Port already in use**
```bash
# Change port in .env
STREAMLIT_SERVER_PORT=8502

# Or manually
streamlit run main.py --server.port=8502
```

### **API rate limits**
- Sign up for Alpha Vantage free API: https://www.alphavantage.co/
- Get API key and add to `.env`
- Free tier: 5 calls per minute, 500 per day

### **Permission denied on Linux**
```bash
chmod +x setup.sh
./setup.sh
```

---

## Requirements

- Python 3.8+ (3.11 recommended)
- pip or conda
- 200MB disk space
- Internet connection (for stock data)

---

## Support

For issues:
1. Check `.env` file is properly configured
2. Ensure virtual environment is activated
3. Check Python version: `python --version`
4. Check logs: `streamlit run main.py`

