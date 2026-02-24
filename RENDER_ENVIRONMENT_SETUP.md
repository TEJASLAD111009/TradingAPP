# Render Environment Variables Setup Guide

## Required Environment Variables

Set these in your Render dashboard under **Environment**:

### Critical Variables (Must Be Set)
```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
PYTHONUNBUFFERED=true
```

### Optional Variables (Already Configured)
```
BASE_CURRENCY=USD
CONVERSION_CURRENCY=INR
INITIAL_WALLET_BALANCE=1000.0
YFINANCE_ENABLED=true
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 🔑 How to Get API Keys

### Alpha Vantage API Key (For Stock Data)
1. Go to **[alphavantage.co](https://www.alphavantage.co)**
2. Click **"GET FREE API KEY"**
3. Enter your email and click **"GET FREE API KEY"**
4. Check your email for the API key
5. Set `ALPHA_VANTAGE_API_KEY` in Render environment with that key

**Note:** Free tier has rate limits (5 requests/minute)

---

## Environment Variable Configuration Steps

### Method 1: Render Dashboard (Recommended)
1. Go to your Render service dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. For each variable:
   - **Key:** `ALPHA_VANTAGE_API_KEY` (or other variable name)
   - **Value:** Paste your actual API key
5. Click **"Save"**
6. Render automatically redeploys with new environment variables

### Method 2: Using .env File (Local Testing)
Create a `.env` file in your project root:
```env
ALPHA_VANTAGE_API_KEY=M856UB65N7IOCGDM
BASE_CURRENCY=USD
CONVERSION_CURRENCY=INR
INITIAL_WALLET_BALANCE=1000.0
YFINANCE_ENABLED=true
PYTHONUNBUFFERED=true
```

**Note:** `.env` is in `.gitignore` - it won't be deployed to Render. Always set production keys in Render dashboard.

---

## ✅ Verification Checklist

After setting environment variables:

- [ ] `ALPHA_VANTAGE_API_KEY` is set in Render
- [ ] `PYTHONUNBUFFERED=true` is set
- [ ] App has redeployed (check Render logs)
- [ ] App loads without errors
- [ ] Login works with demo/demo123
- [ ] Stock data loads when you search for a symbol
- [ ] Portfolio and wallet features work

---

## 🐛 Environment Variable Troubleshooting

### Issue: Stock data not loading
**Cause:** API key not set or invalid
**Solution:**
1. Verify `ALPHA_VANTAGE_API_KEY` is set in Render
2. Verify it's the correct API key from alphavantage.co
3. Check if you're hitting rate limits (5 req/min on free tier)
4. Fallback: App will try yfinance API if Alpha Vantage fails

### Issue: Different currency values on production vs local
**Cause:** `BASE_CURRENCY` or `CONVERSION_CURRENCY` different
**Solution:**
1. Verify both currency variables match between local `.env` and Render
2. Typically: `BASE_CURRENCY=USD` and `CONVERSION_CURRENCY=INR`

### Issue: Different wallet balance on production
**Cause:** `INITIAL_WALLET_BALANCE` set differently
**Solution:**
1. Check Render environment vs local `.env`
2. Typically: `INITIAL_WALLET_BALANCE=1000.0`
3. Change in Render dashboard and redeploy

### Issue: App crashes with encoding errors
**Cause:** `PYTHONUNBUFFERED` not set
**Solution:**
1. Set `PYTHONUNBUFFERED=true` in Render environment
2. Redeploy the app

---

## 📝 Default Test Credentials

Always available (created automatically):
- `demo` / `demo123`
- `trader` / `trader123`
- `user` / `password123`

---

## 🔄 Updating Environment Variables

To update a variable:
1. Go to Render dashboard
2. Click your service
3. Click **"Environment"** tab
4. Find the variable to update
5. Click the value to edit it
6. Update and save
7. Render automatically redeploys

---

## 📊 Configuration Summary

| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `ALPHA_VANTAGE_API_KEY` | Stock API access | demo | Yes* |
| `PYTHONUNBUFFERED` | Real-time logs | true | Yes |
| `BASE_CURRENCY` | Main currency | USD | No |
| `CONVERSION_CURRENCY` | Conversion target | INR | No |
| `INITIAL_WALLET_BALANCE` | New user balance | 1000.0 | No |
| `YFINANCE_ENABLED` | Enable yfinance fallback | true | No |

*Can use "demo" key but has very low rate limits

---

## 💡 Best Practices

1. **Never commit API keys** - Always use Render environment variables
2. **Keep `.env` local** - Add to `.gitignore` (already done)
3. **Test locally first** - Verify with local `.env` before pushing
4. **Use strong API keys** - Get your own key from alphavantage.co
5. **Monitor rate limits** - Track API usage to avoid hitting limits
6. **Document changes** - Note when you change environment variables

---

## 🆘 Still Having Issues?

1. **Check Render Logs:** Go to your service and click "Logs" for detailed errors
2. **Verify all variables:** Make sure no typos in variable names
3. **Redeploy:** Sometimes a fresh deploy fixes environment issues
4. **Check dependencies:** Ensure all Python packages are in `requirements.txt`
5. **Try local first:** Test with `streamlit run main.py` locally before troubleshooting on Render

---

## 📚 Related Documentation

- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Streamlit Configuration](https://docs.streamlit.io/library/advanced-features/configuration)
- [Alpha Vantage API Docs](https://www.alphavantage.co/documentation/)
- [YFinance Documentation](https://yfinance.readthedocs.io/)

Your Trading App should now be fully configured for Render! 🚀
