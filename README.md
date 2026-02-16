# Trading App - MVC Architecture

A refactored version of the Streamlit trading app using the Model-View-Controller (MVC) architectural pattern.

## Project Structure

```
trading-app/
├── models/                 # Data models and business logic
│   ├── user.py            # User authentication model
│   ├── portfolio.py       # Portfolio and balance management
│   └── __init__.py
├── views/                 # Streamlit UI components
│   ├── auth_view.py       # Login/register view
│   ├── dashboard_view.py  # Main dashboard view
│   └── __init__.py
├── controllers/           # Application controllers
│   ├── app_controller.py  # Main app controller
│   └── __init__.py
├── utils/                 # Utility functions
│   ├── api_client.py      # Stock API client
│   └── __init__.py
├── app.py                 # Entry point
├── code.py               # Original (legacy) code
└── requirements.txt      # Dependencies
```

## Architecture Explanation

### Models (Business Logic)
- **user.py**: Handles user authentication and validation
  - `authenticate()`: Verifies credentials
  - `register_user()`: Creates new users
  
- **portfolio.py**: Manages portfolio and balance data
  - `get_balance()`: Retrieves user balance
  - `add_to_portfolio()`: Processes stock purchases
  - `remove_from_portfolio()`: Processes stock sales

### Views (UI Components)
- **auth_view.py**: Authentication interface
  - `show_login()`: Login form
  - `show_register()`: Registration form
  - `show_logout()`: Logout button
  
- **dashboard_view.py**: Main trading interface
  - `show_header()`: Balance display
  - `show_stock_data_section()`: Stock lookup
  - `display_stock_chart()`: Chart visualization
  - `show_buy_sell_section()`: Trading form
  - `display_portfolio()`: Portfolio view

### Controllers (Application Flow)
- **app_controller.py**: Main orchestrator
  - `run()`: Main execution loop
  - `show_login_page()`: Authentication flow
  - `show_main_app()`: Trading interface flow
  - `process_trade()`: Transaction handling

### Utils (Helper Functions)
- **api_client.py**: Alpha Vantage API integration
  - `fetch_intraday_data()`: Get intraday stock data
  - `fetch_daily_data()`: Get daily stock data

## Running the App

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Key Benefits of MVC Architecture

✅ **Separation of Concerns**: Models, Views, and Controllers are independent
✅ **Reusability**: Components can be reused across the application
✅ **Testability**: Each component can be tested independently
✅ **Maintainability**: Easier to locate and fix bugs
✅ **Scalability**: Simple to add new features without affecting existing code
✅ **Code Organization**: Clear structure makes onboarding easier

## Future Enhancements

- Replace in-memory storage with a real database (PostgreSQL, MongoDB)
- Add data persistence with JSON/CSV files
- Implement advanced charts with Plotly
- Add portfolio analytics and performance metrics
- Implement real-time stock price updates
- Add more authentication methods (OAuth, email verification)
- Unit tests for each component
