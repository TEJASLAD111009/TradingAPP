# Trading App - Stock Data Not Loading on Render - Troubleshooting Guide

## Problem
Stock data shows: "Unable to fetch stock data. Please try again later."

---

## Root Causes & Solutions

### 1. ❌ Network/API Connectivity Issues on Render

**Why it happens:**
- Render may have firewall restrictions
- yfinance API may be blocking requests from cloud servers
- Exchange rate API temporarily unavailable

**How to fix:**

#### Step 1: Check Render Logs
1. Go to your Render service dashboard
2. Click **"Logs"** tab
3. Look for lines with:
   - `Error fetching stock`
   - `yfinance error`
   - `Fetching stock data for: AAPL`

#### Step 2: Run Diagnostics Script
```bash
# SSH into your Render instance or run this locally with:
python -m utils.diagnostics
```

Expected output should show:
```
TRADING APP - API DIAGNOSTICS REPORT
====================================
Network: OK
yfinance: OK
exchange_rate: OK
Overall Status: OK
```

#### Step 3: Check Specific Errors
Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection timeout` | Network blocked | Contact Render support or use alternative API |
| `Empty data returned` | API rate limited | Implement retry logic or use cached data |
| `401/403 error` | API key issue | Verify API keys in environment |
| `DNS resolution failed` | Render network issue | Restart the service |

---

### 2. ❌ yfinance Specific Issues

**Problem:** yfinance not working on Render

**Solutions:**

#### Option A: Add timeout handling
Already implemented in updated code - increases stability

#### Option B: Use alternative data source
Future enhancement: Could add fallback to finviz or other free APIs

#### Option C: Cache stock data
Reduce API calls by caching data on disk:
```python
# Example (future enhancement)
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_stock_price_cached(symbol):
    return StockAPI.get_stock_price(symbol)
```

---

### 3. ❌ Exchange Rate API Issues

**Problem:** Can't convert USD to INR

**Error signs in logs:**
```
Error fetching exchange rate: [network error]
Using default exchange rate: 1 USD = ₹83.0
```

**Solution:**
- App automatically falls back to default rate (₹83.0)
- Still functional but may not be current rate
- Exchange rate cached for 1 hour to reduce calls

---

## Debugging Steps

### Step 1: Enable Debug Mode in Render

Add to environment variables:
```
STREAMLIT_LOGGER_LEVEL=debug
PYTHONUNBUFFERED=true
```

### Step 2: Check Logs in Real-time

```bash
# View last 100 lines of logs
render logs [your-service-name] | tail -100

# Filter for stock-related errors
render logs [your-service-name] | grep -i "stock"
```

### Step 3: Test Individual APIs Locally

```python
# Test yfinance
python -c "import yfinance as yf; print(yf.Ticker('AAPL').history(period='1d'))"

# Test exchange rate
python -c "import requests; r=requests.get('https://api.exchangerate-api.com/v4/latest/USD'); print(r.json()['rates']['INR'])"
```

### Step 4: Check Network from Render Container

```bash
# SSH into Render and test connectivity
curl https://query1.finance.yahoo.com/v10/finance/quoteSummary/AAPL
curl https://api.exchangerate-api.com/v4/latest/USD
```

---

## Improved Error Handling (Already Implemented)

### What's been fixed:

1. **✅ Better logging** - All API calls logged to console/Render logs
   ```python
   logger.info(f"Fetching stock data for: {symbol}")
   logger.error(f"Error fetching stock {symbol}: {str(e)}")
   ```

2. **✅ Detailed error messages to user**
   - Instead of generic "Unable to fetch stock data"
   - Now shows specific reasons and tips
   - User sees troubleshooting suggestions

3. **✅ Diagnostics on startup**
   - Runs connection tests on app load
   - Reports status in Render logs
   - Helps identify issues early

4. **✅ Graceful fallbacks**
   - Uses cached exchange rate if current fails
   - Defaults to ₹83.0 if all APIs fail
   - App remains functional

---

## Monitoring & Logging

### View Logs in Render

**Real-time logs:**
```
Service Dashboard → Logs → (streaming in real-time)
```

**Key log lines to watch for:**
```
Fetching data for 15 stocks...          ← Good sign
Successfully fetched 15/15 stocks       ← Perfect
Successfully fetched AAPL: $185.42       ← Individual stock loaded
Error fetching stock AAPL: [error]      ← Problem with specific stock
Fetching data for 15 stocks...
Successfully fetched 3/15 stocks        ← Partial failure
```

---

## Testing

### Local Testing (Before Deploying)

```bash
# Test with .env file
streamlit run main.py --logger.level=debug

# Check if stocks load
# 1. Navigate to "📊 Stock Market" tab
# 2. Check "🔍 View Stocks" tab
# 3. Should see table of popular stocks
```

### Render Testing (After Deploying)

1. Open your Render app URL
2. Login with demo/demo123
3. Go to "📊 Stock Market"
4. Check if stocks appear
5. Try searching for a specific stock
6. If error: Check Render Logs for details

---

## Fallback Strategies (If APIs Consistently Fail)

### Option 1: Use Cached Data
Store a local copy of stock prices:
```python
# data/stock_cache.json
{
    "AAPL": 185.42,
    "MSFT": 330.05,
    ...
}
```

### Option 2: Use Different API
Consider alternatives:
- Alpha Vantage (requires API key)
- IEX Cloud (paid service)
- Polygon.io (limited free tier)
- Finnhub (free with API key)

### Option 3: Hybrid Approach
Try multiple APIs in sequence:
1. Try yfinance
2. If fails, try Alpha Vantage
3. If fails, use cached data
4. If all fail, show demo data

---

## Performance Optimization

Current implementation already includes:

1. **Caching**
   - Exchange rate cached for 1 hour
   - Session state for user preferences
   - Streamlit cache decorators

2. **Error Handling**
   - Timeouts to prevent hanging
   - Exception catching to prevent crashes
   - Graceful fallbacks

3. **Async-friendly** (Future)
   - Could add concurrent requests for speed
   - Currently sequential (safer on Render)

---

## Render-Specific Configuration

### render.yaml Settings

Already configured with:
```yaml
startCommand: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
```

**Key settings:**
- `server.headless=true` - Required for Render
- `server.port=$PORT` - Uses Render's dynamic port
- `server.address=0.0.0.0` - Listen on all interfaces

---

## Still Having Issues?

### Quick Checklist

- [ ] Render logs show no critical errors
- [ ] Network connectivity test passes
- [ ] yfinance responding (test locally)
- [ ] Exchange rate API responding
- [ ] No firewall blocking outbound requests
- [ ] App restarted after environment changes

### Get Help

1. **Check Render Logs** - Most detailed info about failures
2. **Run Diagnostics** - `python -m utils.diagnostics`
3. **Test Locally** - Ensure APIs work on your machine
4. **Check Status Pages** - Is yfinance having outages?

---

## Prevention Tips

1. **Monitor logs regularly** - Catch issues early
2. **Test after updates** - Verify stock loading works
3. **Use caching** - Reduce API calls and failures
4. **Have fallbacks** - Don't rely on single API
5. **Document issues** - Track what works/doesn't work

---

## Implementation Summary

Your app now includes:

✅ Comprehensive logging at every step  
✅ Better error messages shown to users  
✅ Diagnostic tools to identify issues  
✅ Graceful fallbacks when APIs fail  
✅ Environment-aware error handling  
✅ Detailed troubleshooting guide  

**Result:** Stock data issues are now much easier to diagnose and fix! 🚀
