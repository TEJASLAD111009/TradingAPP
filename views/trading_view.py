"""Streamlit views for trading operations."""
import streamlit as st
from controllers import PortfolioController
from utils import StockAPI
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def portfolio_page(username: str):
    """Display portfolio page."""
    st.title("📈 My Portfolio")
    
    # Get exchange rate
    exchange_rate = StockAPI.get_exchange_rate()
    
    # Get portfolio data
    portfolio_data = PortfolioController.get_portfolio(username)
    holdings = portfolio_data['holdings']
    total_value = portfolio_data['total_value']
    total_invested = portfolio_data['total_invested']
    total_profit_loss = portfolio_data['total_profit_loss']
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Value",
            value=f"${total_value:,.2f}",
            delta=f"₹{total_value * exchange_rate:,.0f}"
        )
    
    with col2:
        st.metric(
            label="💵 Total Invested",
            value=f"${total_invested:,.2f}",
            delta=f"₹{total_invested * exchange_rate:,.0f}"
        )
    
    with col3:
        color = "green" if total_profit_loss >= 0 else "red"
        delta_text = f"{(total_profit_loss/total_invested*100):.2f}%" if total_invested > 0 else "0%"
        st.metric(
            label="📈 Total P/L",
            value=f"${total_profit_loss:,.2f}",
            delta=f"₹{total_profit_loss * exchange_rate:,.0f} ({delta_text})"
        )
    
    with col4:
        num_stocks = len(holdings)
        st.metric(label="📁 Holdings", value=num_stocks)
    
    st.divider()
    
    # Holdings table
    if holdings:
        st.subheader("Your Holdings")
        
        holdings_data = []
        for symbol, stock in holdings.items():
            holdings_data.append({
                'Symbol': symbol,
                'Quantity': stock.quantity,
                'Avg Cost (USD)': f"${stock.purchase_price:,.2f}",
                'Avg Cost (INR)': f"₹{stock.purchase_price * exchange_rate:,.0f}",
                'Current Price (USD)': f"${stock.current_price:,.2f}",
                'Current Price (INR)': f"₹{stock.current_price * exchange_rate:,.0f}",
                'Total Value (USD)': f"${stock.get_total_value():,.2f}",
                'Total Value (INR)': f"₹{stock.get_total_value() * exchange_rate:,.0f}",
                'P/L (USD)': f"${stock.get_profit_loss():,.2f}",
                'P/L %': f"{stock.get_profit_loss_percentage():.2f}%"
            })
        
        df_holdings = pd.DataFrame(holdings_data)
        st.dataframe(df_holdings, use_container_width=True, hide_index=True)
        
        # Portfolio pie chart
        st.subheader("Portfolio Allocation")
        
        allocation_data = [
            {
                'symbol': symbol,
                'value': stock.get_total_value()
            }
            for symbol, stock in holdings.items()
        ]
        
        if allocation_data:
            fig = px.pie(
                allocation_data,
                values='value',
                names='symbol',
                title="Asset Allocation (USD)"
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 Your portfolio is empty. Start trading to build your portfolio!")


def stocks_page(username: str):
    """Display stocks browsing and trading page."""
    st.title("📊 Stock Market")
    
    exchange_rate = StockAPI.get_exchange_rate()
    
    tab1, tab2, tab3 = st.tabs(["🔍 View Stocks", "🛒 Buy Stock", "💳 Sell Stock"])
    
    with tab1:
        st.subheader("Popular US Stocks")
        st.info(f"💹 Currency Exchange Rate: 1 USD = ₹{exchange_rate:.2f}")
        
        # Get popular stocks
        with st.spinner("Fetching stock data..."):
            popular_stocks = PortfolioController.get_popular_stocks()
        
        if popular_stocks:
            stocks_data = []
            for symbol, stock_data in popular_stocks.items():
                stocks_data.append({
                    'Symbol': symbol,
                    'Company': stock_data['name'][:30],
                    'Price (USD)': f"${stock_data['price_usd']:,.2f}",
                    'Price (INR)': f"₹{stock_data['price_inr']:,.0f}",
                    'Change': f"{stock_data['change']:.2f}",
                    'Change %': f"{stock_data['change_percent']:.2f}%",
                    'Market Cap': stock_data['market_cap'],
                    'P/E Ratio': stock_data['pe_ratio']
                })
            
            df_stocks = pd.DataFrame(stocks_data)
            st.dataframe(df_stocks, use_container_width=True, hide_index=True)
        else:
            st.error("Unable to fetch stock data. Please try again later.")
    
    with tab2:
        st.subheader("Buy Stock")
        
        col1, col2 = st.columns(2)
        
        with col1:
            buy_symbol = st.text_input(
                "Stock Symbol",
                placeholder="e.g., AAPL",
                value="AAPL"
            ).upper()
        
        with col2:
            buy_quantity = st.number_input(
                "Quantity",
                min_value=1,
                step=1,
                value=1
            )
        
        if buy_symbol:
            # Get stock price
            stock_data = PortfolioController.get_stock_data(buy_symbol)
            
            if stock_data:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Price per Share (USD)", f"${stock_data['price_usd']:,.2f}")
                
                with col2:
                    st.metric("Price per Share (INR)", f"₹{stock_data['price_inr']:,.0f}")
                
                with col3:
                    total_cost = stock_data['price_usd'] * buy_quantity
                    st.metric("Total Cost (USD)", f"${total_cost:,.2f}")
                
                with col4:
                    from controllers import WalletController
                    balance = WalletController.get_balance(username)
                    st.metric("Your Balance", f"${balance:,.2f}")
                
                st.info(f"💹 Total Cost in INR: ₹{total_cost * exchange_rate:,.0f}")
                
                if st.button(f"✅ Buy {buy_quantity} shares of {buy_symbol}", use_container_width=True):
                    success, message = PortfolioController.buy_stock(
                        username,
                        buy_symbol,
                        buy_quantity
                    )
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.warning(f"Stock symbol '{buy_symbol}' not found. Please check the symbol.")
    
    with tab3:
        st.subheader("Sell Stock")
        
        # Get portfolio
        portfolio_data = PortfolioController.get_portfolio(username)
        holdings = portfolio_data['holdings']
        
        if not holdings:
            st.info("You don't have any stocks to sell.")
        else:
            # Get symbols for dropdown
            available_symbols = list(holdings.keys())
            
            col1, col2 = st.columns(2)
            
            with col1:
                sell_symbol = st.selectbox(
                    "Select Stock to Sell",
                    available_symbols
                )
            
            with col2:
                if sell_symbol:
                    max_quantity = holdings[sell_symbol].quantity
                    sell_quantity = st.number_input(
                        f"Quantity (Max: {max_quantity})",
                        min_value=1,
                        max_value=max_quantity,
                        step=1,
                        value=1
                    )
                else:
                    sell_quantity = 1
            
            if sell_symbol:
                stock_data = PortfolioController.get_stock_data(sell_symbol)
                
                if stock_data:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Current Price (USD)", f"${stock_data['price_usd']:,.2f}")
                    
                    with col2:
                        st.metric("Current Price (INR)", f"₹{stock_data['price_inr']:,.0f}")
                    
                    with col3:
                        total_proceeds = stock_data['price_usd'] * sell_quantity
                        st.metric("Total Proceeds (USD)", f"${total_proceeds:,.2f}")
                    
                    with col4:
                        cost_basis = holdings[sell_symbol].purchase_price * sell_quantity
                        st.metric("Cost Basis (USD)", f"${cost_basis:,.2f}")
                    
                    st.info(f"💹 Proceeds in INR: ₹{total_proceeds * exchange_rate:,.0f}")
                    
                    if st.button(f"✅ Sell {sell_quantity} shares of {sell_symbol}", use_container_width=True):
                        success, message = PortfolioController.sell_stock(
                            username,
                            sell_symbol,
                            int(sell_quantity)
                        )
                        if success:
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)


def stock_details_page(username: str):
    """Display detailed information about a stock."""
    st.title("📈 Stock Details")
    
    exchange_rate = StockAPI.get_exchange_rate()
    
    symbol = st.text_input(
        "Enter Stock Symbol",
        value="AAPL",
        placeholder="e.g., AAPL"
    ).upper()
    
    if symbol:
        with st.spinner(f"Fetching data for {symbol}..."):
            stock_data = PortfolioController.get_stock_data(symbol)
        
        if stock_data:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Company", stock_data['name'][:20])
            
            with col2:
                st.metric("Price (USD)", f"${stock_data['price_usd']:,.2f}")
            
            with col3:
                st.metric("Price (INR)", f"₹{stock_data['price_inr']:,.0f}")
            
            with col4:
                st.metric("24h Change %", f"{stock_data['change_percent']:.2f}%")
            
            st.divider()
            
            # Exchange rate info
            st.info(f"💹 Exchange Rate: 1 USD = ₹{exchange_rate:.2f} (Last Updated: {stock_data['updated_at'][:16]})")
            
            st.divider()
            
            # Additional info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"**Market Cap**\n{stock_data['market_cap']}")
            
            with col2:
                st.info(f"**P/E Ratio**\n{stock_data['pe_ratio']}")
            
            with col3:
                st.info(f"**Dividend Yield**\n{stock_data['divi_yield']}")
            
            st.divider()
            
            # Historical chart
            st.subheader("Price History")
            
            period = st.selectbox(
                "Select Period",
                ["1mo", "3mo", "6mo", "1y"],
                index=0
            )
            
            with st.spinner("Fetching historical data..."):
                history = PortfolioController.get_stock_history(symbol, period)
            
            if history is not None:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history.index,
                    y=history['Close'],
                    mode='lines',
                    name='Close Price (USD)',
                    line=dict(color='#1f77b4')
                ))
                
                fig.update_layout(
                    title=f"{symbol} Price Chart (USD)",
                    xaxis_title="Date",
                    yaxis_title="Price (USD)",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show price range info
                st.divider()
                st.subheader("Price Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Period High (USD)", f"${history['High'].max():,.2f}")
                
                with col2:
                    st.metric("Period Low (USD)", f"${history['Low'].min():,.2f}")
                
                with col3:
                    st.metric("Period High (INR)", f"₹{history['High'].max() * exchange_rate:,.0f}")
                
                with col4:
                    st.metric("Period Low (INR)", f"₹{history['Low'].min() * exchange_rate:,.0f}")
        else:
            st.error(f"Stock symbol '{symbol}' not found.")
