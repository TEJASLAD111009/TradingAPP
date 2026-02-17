# MVC Architecture Migration Guide

## Original Code Issues
The original `code.py` had all logic mixed together:
- ❌ UI (Streamlit) mixed with business logic
- ❌ Hard to test individual components
- ❌ Difficult to reuse code
- ❌ Hard to maintain and scale

## New MVC Structure Benefits

### Before (Monolithic)
```
code.py (137 lines)
├── Data (users_db, portfolio, balances)
├── Business Logic (buy_stock, sell_stock, fetch_stock_data)
├── UI (login, logout, main_app)
└── Controllers (all mixed together)
```

### After (MVC)
```
Models/ (Pure Python - Business Logic)
├── user.py → User authentication
└── portfolio.py → Balance & portfolio management

Views/ (Streamlit Components - UI Only)
├── auth_view.py → Login/logout interface
└── dashboard_view.py → Trading interface

Controllers/ (Application Flow - Orchestration)
└── app_controller.py → Coordinates models & views

Utils/ (Helpers)
└── api_client.py → External API integration

app.py (Entry Point - 30 lines)
```

## Code Mapping (Original → New Structure)

### Original Functions → New Model Methods

#### User Authentication (code.py lines 68-75)
```python
# OLD: login() function in main code
def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in users_db and users_db[username] == password:
            st.sidebar.success("Login Successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
```

```python
# NEW: UserModel.authenticate() in models/user.py
def authenticate(self, username: str, password: str) -> bool:
    if username in self.users_db:
        return self.users_db[username] == password
    return False
```

#### Stock Data Fetching (code.py lines 18-31)
```python
# OLD: fetch_stock_data() function in main code
def fetch_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if "Time Series (5min)" in data:
        df = pd.DataFrame(data["Time Series (5min)"]).transpose()
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df = df.astype(float)
        return df
```

```python
# NEW: StockAPIClient.fetch_intraday_data() in utils/api_client.py
def fetch_intraday_data(self, symbol: str, interval: str = "5min") -> Optional[pd.DataFrame]:
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": self.api_key,
    }
    try:
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Time Series (5min)" in data:
            df = pd.DataFrame(data["Time Series (5min)"]).transpose()
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            df = df.astype(float)
            return df
```

#### Buy Stock (code.py lines 34-44)
```python
# OLD: buy_stock() function in main code
def buy_stock(username, symbol, quantity, price):
    global portfolio, balances
    cost = quantity * price
    if balances[username] >= cost:
        balances[username] -= cost
        portfolio[username].append({
            "symbol": symbol, 
            "quantity": quantity, 
            "price": price,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        st.success(f"Successfully bought {quantity} shares of {symbol} for Rs {cost:.2f}")
    else:
        st.error("Insufficient balance to complete this transaction.")
```

```python
# NEW: PortfolioModel.add_to_portfolio() in models/portfolio.py
def add_to_portfolio(self, username: str, symbol: str, quantity: int, price: float) -> bool:
    cost = quantity * price
    
    if self.balances.get(username, 0) < cost:
        return False
    
    self.balances[username] -= cost
    
    if username not in self.portfolio:
        self.portfolio[username] = []
    
    self.portfolio[username].append({
        "symbol": symbol,
        "quantity": quantity,
        "price": price,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    return True
```

#### Sell Stock (code.py lines 47-58)
```python
# OLD: sell_stock() function in main code
def sell_stock(username, symbol, quantity, price):
    global portfolio, balances
    user_stocks = portfolio.get(username, [])
    for stock in user_stocks:
        if stock["symbol"] == symbol and stock["quantity"] >= quantity:
            stock["quantity"] -= quantity
            balances[username] += quantity * price
            if stock["quantity"] == 0:
                user_stocks.remove(stock)
            st.success(f"Successfully sold {quantity} shares of {symbol} for Rs {quantity * price:.2f}")
            return
    st.error("You do not own enough shares of this stock.")
```

```python
# NEW: PortfolioModel.remove_from_portfolio() in models/portfolio.py
def remove_from_portfolio(self, username: str, symbol: str, quantity: int, price: float) -> bool:
    if username not in self.portfolio:
        return False
    
    user_stocks = self.portfolio[username]
    
    for stock in user_stocks:
        if stock["symbol"] == symbol:
            if stock["quantity"] >= quantity:
                stock["quantity"] -= quantity
                self.balances[username] += quantity * price
                
                if stock["quantity"] == 0:
                    user_stocks.remove(stock)
                
                return True
    
    return False
```

## New Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| `models/user.py` | User authentication logic | 46 |
| `models/portfolio.py` | Portfolio management logic | 129 |
| `utils/api_client.py` | Stock API integration | 89 |
| `views/auth_view.py` | Authentication UI (Streamlit) | 65 |
| `views/dashboard_view.py` | Dashboard UI (Streamlit) | 104 |
| `controllers/app_controller.py` | App orchestration & flow | 120 |
| `app.py` | Entry point | 30 |

**Total: ~583 lines of well-organized, maintainable code**

## Migration Steps for Existing Code

To migrate from original code to MVC:
1. ✅ Extract models (user, portfolio) → `models/`
2. ✅ Extract API calls → `utils/`
3. ✅ Create Streamlit views → `views/`
4. ✅ Create controller → `controllers/`
5. ✅ Create main entry point → `app.py`

## Running the New Version

```bash
# Install dependencies
pip install -r requirements.txt

# Run the MVC version
streamlit run app.py
```

## Testing Benefits

Each component can now be tested independently:

```python
# Test model logic without Streamlit
from models.portfolio import PortfolioModel

portfolio = PortfolioModel()
portfolio.initialize_user("test_user", 10000)
success = portfolio.add_to_portfolio("test_user", "AAPL", 10, 150)
assert success == True
assert portfolio.get_balance("test_user") == 8500
```

This is much cleaner than testing the original monolithic code!
