# MVC Architecture Diagram

## Data Flow in the Application

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRY POINT: app.py                          │
│         (30 lines - Streamlit Configuration)                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONTROLLER: app_controller.py                       │
│  - Orchestrates the entire application flow                     │
│  - Handles user interactions                                    │
│  - Coordinates between Models and Views                         │
│                                                                 │
│  Main Methods:                                                  │
│  • run() - Main execution loop                                  │
│  • show_login_page() - Auth flow                               │
│  • show_main_app() - Trading flow                              │
│  • process_trade() - Transaction handling                       │
└────────────────┬──────────────────────────┬──────────────────────┘
                 │                          │
        ┌────────▼─────────┐      ┌────────▼─────────┐
        │  MODELS (Logic)  │      │   VIEWS (UI)     │
        └──────────────────┘      └──────────────────┘
        │                         │
┌───────┼──────────────────┐  ┌──┼──────────────────┐
│   models/user.py         │  │  views/auth_view.py│
│   ─────────────────       │  │  ──────────────────│
│   • authenticate()        │  │  • show_login()    │
│   • user_exists()         │  │  • show_register() │
│   • register_user()       │  │  • show_logout()   │
│                           │  │                    │
│   models/portfolio.py     │  │  views/dash...py   │
│   ──────────────────      │  │  ──────────────────│
│   • get_balance()         │  │  • show_header()   │
│   • get_portfolio()       │  │  • display_chart() │
│   • add_to_portfolio()    │  │  • show_form()     │
│   • remove_from_...()     │  │  • display_...()   │
└──────────────┬───────────┘  └────────┬───────────┘
               │                       │
               └───────────┬───────────┘
                           │
                    ┌──────▼──────┐
                    │   UTILS     │
                    │─────────────│
                    │api_client.py│
                    │─────────────│
                    │• fetch_    │
                    │  intraday()│
                    │• fetch_   │
                    │  daily()  │
                    └────────────┘
```

## Application Flow Sequence

### 1. LOGIN FLOW
```
User Launches App (app.py)
         │
         ▼
    Controller.run()
         │
         ├─► Check session state
         │
         └─► show_login_page()
              │
              ├─► AuthView.show_login()
              │   └─► Render login form
              │
              └─► User enters credentials
                  │
                  ▼
              UserModel.authenticate()
              │
              ├─► True  → Initialize portfolio → show_main_app()
              │
              └─► False → Show error message
```

### 2. TRADING FLOW
```
User in Main App (show_main_app())
         │
         ├─► Tab 1: Stock Data
         │   ├─► DashboardView.show_stock_data_section()
         │   │   └─► User enters symbol
         │   │
         │   └─► StockAPIClient.fetch_intraday_data()
         │       └─► Display chart & data
         │
         ├─► Tab 2: Buy/Sell Trade
         │   ├─► DashboardView.show_buy_sell_section()
         │   │   └─► User submits trade
         │   │
         │   └─► Controller.process_trade()
         │       │
         │       ├─► Buy: PortfolioModel.add_to_portfolio()
         │       │   ├─► Check balance
         │       │   ├─► Update balance
         │       │   └─► Add stock to portfolio
         │       │
         │       └─► Sell: PortfolioModel.remove_from_portfolio()
         │           ├─► Check shares owned
         │           ├─► Update balance
         │           └─► Remove stock from portfolio
         │
         └─► Tab 3: View Portfolio
             └─► DashboardView.display_portfolio()
                 └─► Show portfolio data
```

## Component Interactions

```
┌──────────────────┐
│  USER INTERFACE  │
│  (Streamlit)     │
└────────┬─────────┘
         │
         │ (User clicks button)
         ▼
┌──────────────────────────┐
│   VIEWS (auth_view.py,   │
│   dashboard_view.py)     │
│ (Renders forms, charts)  │
└────────┬─────────────────┘
         │
         │ (Form data)
         ▼
┌──────────────────────────┐
│   CONTROLLER             │
│   (app_controller.py)    │
│ (Processes requests)     │
└─┬──────────────────────┬─┘
  │                      │
  │ (Calls methods)      │ (Calls methods)
  ▼                      ▼
┌──────────────┐   ┌─────────────────┐
│   MODELS     │   │   UTILS         │
│ (user.py,   │   │ (api_client.py) │
│  portfo...) │   │ (API calls)      │
│ (Business   │   └─────────────────┘
│  logic)     │
└──────┬───────┘
       │
       │ (Return results)
       ▼
    DATABASE/STATE
(users_db, portfolio, balances)
```

## File Structure Tree

```
trading-app/
│
├── app.py                          ⭐ ENTRY POINT
│   └── Imports AppController
│
├── controllers/
│   ├── __init__.py
│   └── app_controller.py          🎛️ ORCHESTRATOR
│       ├── Imports all models & views
│       ├── Manages application flow
│       └── Handles user interactions
│
├── models/
│   ├── __init__.py
│   ├── user.py                    📋 USER LOGIC
│   │   └── UserModel class
│   │
│   └── portfolio.py               💰 PORTFOLIO LOGIC
│       └── PortfolioModel class
│
├── views/
│   ├── __init__.py
│   ├── auth_view.py               🔐 AUTH UI
│   │   └── AuthView class
│   │
│   └── dashboard_view.py          📊 DASHBOARD UI
│       └── DashboardView class
│
├── utils/
│   ├── __init__.py
│   └── api_client.py              🌐 API INTEGRATION
│       └── StockAPIClient class
│
├── requirements.txt                📦 DEPENDENCIES
├── README.md                       📚 DOCUMENTATION
├── MIGRATION_GUIDE.md              🔄 MIGRATION HELP
└── code.py                        🗂️ ORIGINAL CODE
```

## Class Relationships

```
AppController
├── has-a UserModel
│   └── authenticate(username, password)
│   └── user_exists(username)
│   └── register_user(username, password)
│
├── has-a PortfolioModel
│   ├── get_balance(username)
│   ├── set_balance(username, amount)
│   ├── get_portfolio(username)
│   ├── add_to_portfolio(username, symbol, quantity, price)
│   └── remove_from_portfolio(username, symbol, quantity, price)
│
├── has-a AuthView
│   ├── show_login()
│   ├── show_register()
│   └── show_logout()
│
├── has-a DashboardView
│   ├── show_header(username)
│   ├── show_stock_data_section()
│   ├── display_stock_chart(data, symbol)
│   ├── show_buy_sell_section()
│   ├── display_portfolio(username)
│   ├── show_success_message(...)
│   └── show_error_message(message)
│
└── has-a StockAPIClient
    ├── fetch_intraday_data(symbol, interval)
    └── fetch_daily_data(symbol)
```

## Advantages of This Architecture

| Aspect | Benefit |
|--------|---------|
| **Separation** | Models never import views or controllers |
| **Testing** | Test business logic without Streamlit |
| **Reusability** | Models can be used in other projects |
| **Maintainability** | Easy to find and fix bugs |
| **Scalability** | Add new features without breaking existing ones |
| **Clarity** | Clear responsibility for each component |
| **Database** | Easy to switch from in-memory to real database |

## Example: How a Trade Request Flows

```
1. User clicks "Submit" on trade form
   ↓
2. DashboardView.show_buy_sell_section() 
   returns form data dict
   ↓
3. AppController.process_trade() receives data
   ↓
4. Validates data
   ↓
5. Calls appropriate PortfolioModel method:
   - add_to_portfolio() for Buy
   - remove_from_portfolio() for Sell
   ↓
6. PortfolioModel updates balances/portfolio
   and returns success/failure boolean
   ↓
7. AppController checks result
   ↓
8. Calls DashboardView to show:
   - show_success_message() if True
   - show_error_message() if False
   ↓
9. UI refreshes with updated data
```

This ensures clean separation between business logic (model), 
presentation (view), and coordination (controller)!
