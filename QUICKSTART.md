# Trading App - Quick Start Guide

Get the Trading App up and running in minutes! 🚀

## ⚡ Fastest Way to Start

### Windows Users

Simply double-click the `setup.bat` file:
```bash
setup.bat
```

This will:
1. ✅ Check Python installation
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Launch the app

### macOS & Linux Users

Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

---

## 🔧 Manual Setup (If Script Doesn't Work)

### Step 1: Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### Step 2: Open Terminal/Command Prompt
- Navigate to the trading folder:
```bash
cd path/to/trading
```

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the App
```bash
streamlit run main.py
```

---

## 🔐 Demo Login

After starting the app, use these credentials to test:

| Username | Password | Type |
|----------|----------|------|
| `demo` | `demo123` | Demo Account |
| `trader` | `trader123` | Alternate Demo |
| `user` | `password123` | Basic User |

**OR** Create your own account using the registration form!

---

## 📝 First Steps in the App

1. **Login or Register**
   - Use demo credentials or create a new account
   - Initial balance: ₹10,000

2. **Explore the Dashboard**
   - Check your balance
   - View portfolio summary
   - See quick action buttons

3. **Browse Stocks**
   - Go to "Stock Market" tab
   - View popular US stocks with live prices
   - Check individual stock details with charts

4. **Buy a Stock**
   - Click "Buy Stock" tab
   - Enter symbol (e.g., AAPL)
   - Enter quantity
   - Review total cost
   - Click "Buy"

5. **Check Your Portfolio**
   - See all holdings and prices
   - Track profit/loss
   - View portfolio allocation pie chart

6. **Manage Wallet**
   - Deposit more funds
   - Check transaction history
   - Monitor balance

---

## 🆘 Troubleshooting

### Issue: "Python not found"
**Solution:** 
- Windows: Make sure Python is added to PATH
- macOS/Linux: Use `python3` instead of `python`

### Issue: Port 8501 already in use
**Solution:**
```bash
streamlit run main.py --server.port 8502
```

### Issue: "No module named streamlit"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Stock prices show "N/A"
**Solution:**
- Check internet connection
- Ensure symbols are valid (e.g., AAPL, MSFT)
- YFinance API is free but has rate limits

### Issue: Data files not showing
**Solution:**
- Files are auto-created on first interaction
- Check `data/` folder permissions

---

## 📊 Popular Stocks to Trade

- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc.
- **AMZN** - Amazon.com Inc.
- **TSLA** - Tesla Inc.
- **META** - Meta Platforms Inc.
- **NVDA** - NVIDIA Corporation
- **JPM** - JPMorgan Chase & Co.
- **V** - Visa Inc.
- **WMT** - Walmart Inc.

---

## 💡 Tips & Tricks

### Add More Initial Funds
- Go to "Wallet" → "Deposit Funds"
- Add ₹5,000, ₹10,000, or more
- Use for trading

### View Stock Performance
- Go to "Stock Details"
- Select time period: 1mo, 3mo, 6mo, 1y
- Hover for detailed price information

### Track Your Returns
- Click "Portfolio" to see:
  - Total invested amount
  - Current portfolio value
  - Total profit/loss percentage
  - Per-stock P/L

### Create New Account
- At login page, scroll to "Create New Account"
- Username: min 3 characters
- Password: min 6 characters
- System auto-creates wallet with ₹10,000

---

## 🌐 Access From Multiple Devices

The app stores data locally. To share across devices:

1. Use cloud deployment (Streamlit Cloud, Heroku)
2. Or sync `data/` folder via Google Drive/Dropbox
3. Or upgrade to database backend

---

## 📚 Learn More

- Full setup instructions: [README.md](README.md)
- Architecture details: [STRUCTURE.md](STRUCTURE.md)
- Code documentation: In-file comments

---

## 🎉 You're Ready!

Start trading and building your portfolio! Remember:
- This is a demo app for educational purposes
- Conduct real research before real investments
- Have fun exploring! 📈

---

**Need Help?** Check README.md for detailed documentation.

**Version:** 1.0 | **Updated:** February 2026
