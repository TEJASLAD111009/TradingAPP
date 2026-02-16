# Trading App - Setup & Deployment Guide

A comprehensive stock trading application built with Streamlit, Python, and following MVC (Model-View-Controller) architecture.

## 🚀 Features

- **🔐 Secure Authentication** - User registration and login system with password hashing
- **💰 Wallet Management** - Deposit and withdraw funds in Indian Rupees (₹)
- **📊 Stock Trading** - Buy and sell US stocks with real-time prices
- **📈 Portfolio Management** - Track investments, profits, and losses
- **💹 Live Stock Data** - Real-time stock prices using YFinance API (free)
- **📉 Interactive Charts** - Historical price charts and portfolio allocation visualizations
- **🎯 MVC Architecture** - Clean separation of concerns (Models, Views, Controllers)

## 📋 System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Windows, macOS, or Linux
- Internet connection for stock data

## ⚙️ Installation & Setup

### Step 1: Clone or Download the Project

```bash
# If you have git
git clone <your-repo-url>
cd trading

# Or if downloading as zip, extract and navigate to the directory
cd trading
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

## 🔐 Demo Credentials

The application comes with demo accounts for testing:

| Username | Password | Notes |
|----------|----------|-------|
| demo | demo123 | Demo trader account |
| trader | trader123 | Alternative demo account |
| user | password123 | Basic user account |

**Note**: You can also create your own account using the registration form.

## 💻 Usage Guide

### 1. Login / Register
- Use demo credentials or create a new account
- Passwords are hashed and stored securely

### 2. Wallet Management
- **Deposit Funds**: Add money to your wallet in Indian Rupees
- **Withdraw Funds**: Withdraw available balance
- **Transaction History**: View all deposits and withdrawals

### 3. Stock Trading
- **Browse Stocks**: View popular US stocks (AAPL, MSFT, GOOGL, etc.)
- **View Details**: Check stock price, market cap, P/E ratio, and historical charts
- **Buy Stocks**: Purchase stocks with your wallet balance
- **Sell Stocks**: Liquidate your holdings at current market price

### 4. Portfolio
- View all your stock holdings
- Track profit/loss on each position
- See total portfolio value and allocation
- Monitor percentage gains/losses

### 5. Stock Details
- Search for any stock by symbol
- View 1 month, 3 month, 6 month, 1 year price history
- Interactive price charts with hover details
- Company information (market cap, P/E ratio, dividend yield)

## 📁 Project Structure

```
trading/
├── main.py                 # Streamlit app entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── STRUCTURE.md           # Detailed architecture documentation
│
├── models/                # Data Models (M in MVC)
│   ├── __init__.py
│   ├── user.py           # User authentication model
│   ├── wallet.py         # Wallet and transactions model
│   └── portfolio.py      # Stock holdings model
│
├── views/                 # Streamlit UI Components (V in MVC)
│   ├── __init__.py
│   ├── auth_view.py      # Login and registration UI
│   ├── wallet_view.py    # Wallet management UI
│   └── trading_view.py   # Portfolio and stock trading UI
│
├── controllers/           # Business Logic (C in MVC)
│   ├── __init__.py
│   └── trading_controller.py  # Authentication, wallet, and trading logic
│
├── utils/                # Utility Functions
│   ├── __init__.py
│   └── stock_api.py      # YFinance API integration
│
├── config/               # Configuration Files
│   └── (Reserved for future use)
│
└── data/                 # Local Data Storage (JSON files)
    ├── users.json       # Registered users and hashed passwords
    ├── wallets.json     # User wallets and transaction history
    └── portfolios.json  # User stock holdings
```

## 🏗️ MVC Architecture Explanation

### Models (data/)
Defines the data structures:
- **User**: User registration and authentication
- **Wallet**: Balance management and transactions
- **Portfolio**: Stock holdings and valuations

### Controllers (controllers/)
Implements business logic:
- **AuthController**: Login and registration logic
- **WalletController**: Fund management operations
- **PortfolioController**: Stock buying/selling and portfolio management

### Views (views/)
Streamlit UI components:
- **auth_view.py**: Login and registration interface
- **wallet_view.py**: Wallet and transaction display
- **trading_view.py**: Portfolio, stock browser, and trading interface

## 💱 Currency Information

- **Base Currency**: Indian Rupees (INR)
- **Stock Prices**: Converted from USD to INR
- **Exchange Rate**: Approximately 1 USD = 83 INR (can be updated in stock_api.py)

## 📊 APIs Used

### YFinance (Free)
- Real-time stock prices
- Historical price data
- Company information
- No API key required!

```python
# Install yfinance
pip install yfinance
```

## 🔒 Security Notes

- Passwords are hashed using SHA-256
- All data stored locally in JSON files
- No sensitive data transmitted to external servers
- For production, consider using a proper database (PostgreSQL, MongoDB)

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. Create a GitHub account and push your code
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Sign up and connect your GitHub repository
4. Select your branch and main.py file
5. Deploy!

### Option 2: Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run main.py --logger.level=error" > Procfile

# Create Heroku app
heroku login
heroku create your-app-name
git push heroku main
```

### Option 3: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

### Option 4: Local VPS/Server

```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone <your-repo-url>
cd trading

# Install dependencies
pip install -r requirements.txt

# Run with screen or nohup
nohup streamlit run main.py --server.port 80 &

# Or use systemd service for permanent deployment
```

## 🐛 Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution**: Install dependencies using `pip install -r requirements.txt`

### Issue: "yfinance: No data found"
**Solution**: Check internet connection and ensure stock symbol is valid

### Issue: Port 8501 already in use
**Solution**: Run on different port: `streamlit run main.py --server.port 8502`

### Issue: Data files not found
**Solution**: The app will auto-create them. Check that the `data/` directory has write permissions

### Issue: Login not working
**Solution**: Ensure users.json exists in data/ folder (it auto-creates on first login)

## 📱 Features Explained

### Real-Time Stock Prices
- Updates from YFinance API
- Prices shown in Indian Rupees
- Automatic USD to INR conversion

### Portfolio Tracking
- Automatic calculation of averages on multiple buys
- Real-time profit/loss calculation
- Historical cost basis tracking

### Wallet System
- Full transaction history
- Separate tracking for deposits, withdrawals, buys, and sells
- Balance validation before transactions

### User Authentication
- Registration with validation
- Password hashing with SHA-256
- Session management

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python MVC Architecture](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
- [YFinance Documentation](https://github.com/ranaroussi/yfinance)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Plotly Documentation](https://plotly.com/python/)

## 📝 Future Enhancements

- [ ] Database backend (PostgreSQL/MongoDB)
- [ ] Email verification for registration
- [ ] Multi-currency support
- [ ] Advanced charting with technical indicators
- [ ] Watchlist feature
- [ ] Machine learning price predictions
- [ ] Options trading
- [ ] Cryptocurrency support
- [ ] Mobile app version
- [ ] Real-time notifications

## 📝 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions:
1. Check the STRUCTURE.md file for detailed architecture
2. Review the code comments in source files
3. Check existing issues on GitHub

## ⚠️ Disclaimer

This is an educational application. It is not intended for real trading. Always:
- Conduct thorough research before real investments
- Understand the risks involved
- Never invest more than you can afford to lose
- Consult with a financial advisor if needed

---

**Happy Trading! 📈**

*Last Updated: February 2026*
