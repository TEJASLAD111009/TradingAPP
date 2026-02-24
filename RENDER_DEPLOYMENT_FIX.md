# Render Deployment Guide - Data Fix

This guide explains the critical fixes made to ensure your Trading App works properly on Render.

## 🔴 Problems Fixed

### 1. **Missing Data Directory Initialization**
**Issue:** Data files were gitignored and not deployed to Render, causing the app to fail when trying to load user data.

**Solution:** 
- Added `.gitkeep` file in `data/` directory so the folder structure is committed to GitHub
- Added automatic initialization on app startup in `main.py`
- Data files (`users.json`, `wallets.json`, `portfolios.json`) are created automatically when needed

### 2. **Missing Render Configuration**
**Issue:** No `render.yaml` file was present for Render deployment.

**Solution:**
- Created `render.yaml` with proper Streamlit configuration
- Configured proper environment variables for production

### 3. **Entry Point Issue**
**Issue:** `app.py` referenced a non-existent `AppController` class
**Solution:** Use `main.py` as the entry point (which contains the correct implementation)

---

## 🚀 Step-by-Step Deployment to Render

### Step 1: Prepare Your GitHub Repository
```bash
# Push all changes to GitHub
git add -A
git commit -m "Fixed Render deployment: Added render.yaml, data initialization, and .gitkeep"
git push origin main
```

### Step 2: Create Render Service
1. Go to **[render.com](https://render.com)**
2. Click **"New"** → **"Web Service"**
3. Select your GitHub repository
4. Fill in the details:
   - **Name:** `trading-app` (or any name)
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** (Leave empty - will use render.yaml)
   - **Start Command:** (Leave empty - will use render.yaml)

### Step 3: Set Environment Variables
In the Render dashboard, go to **Environment** and add:

```
ALPHA_VANTAGE_API_KEY=your_api_key_here
BASE_CURRENCY=USD
CONVERSION_CURRENCY=INR
INITIAL_WALLET_BALANCE=1000.0
YFINANCE_ENABLED=true
PYTHONUNBUFFERED=true
```

**Important:** Replace `your_api_key_here` with your actual API key from [alphavantage.co](https://www.alphavantage.co)

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Render will automatically deploy from your GitHub repository
3. Monitor the deployment in the **Logs** tab

### Step 5: Access Your App
Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

---

## 🔧 How the App Initializes Data on Render

The updated `main.py` now includes automatic initialization:

```python
@st.cache_resource
def initialize_app():
    """Initialize app data files if they don't exist."""
    UserManager.initialize_default_users()

initialize_app()
```

This ensures:
1. ✅ The `data/` directory is created if it doesn't exist
2. ✅ `users.json` is created with default users on first run
3. ✅ Demo credentials work immediately: `demo` / `demo123`
4. ✅ User wallets and portfolios are created automatically when needed

---

## 📝 Default Test Credentials

After deployment, use these credentials to test:

| Username | Password | Role |
|----------|----------|------|
| `demo` | `demo123` | Demo User |
| `trader` | `trader123` | Demo Trader |
| `user` | `password123` | Demo User |

---

## 🐛 Troubleshooting

### App Shows "File not found" Error
**Cause:** Data directory wasn't initialized
**Fix:** Already handled! The app automatically creates it on startup

### Stock Data Not Loading
**Cause:** API key not set or rate limited
**Solution:** 
1. Verify `ALPHA_VANTAGE_API_KEY` is set in Render environment
2. Yfinance is used as fallback (free, no key needed)
3. Check if you've hit API rate limits

### App Crashes on Startup
**Check the logs:**
```bash
# In Render dashboard, click "Logs" to see error messages
```

Common issues:
- Missing environment variables
- Python version mismatch (should be 3.10.13)
- Missing dependencies (check requirements.txt)

### Data Lost After Deployment
**Note:** Render's free tier uses ephemeral storage. Data is lost when the app restarts.

**Solution for Production:**
- Use a database instead of JSON files (PostgreSQL, MongoDB)
- Or upgrade to Render's paid plans with persistent storage

---

## 📊 File Structure Changes

```
TradingAPP/
├── render.yaml              ← NEW: Render deployment config
├── data/
│   ├── .gitkeep            ← NEW: Ensures data/ directory is committed
│   ├── users.json          ← Created automatically on first run
│   ├── wallets.json        ← Created automatically on first run
│   └── portfolios.json     ← Created automatically on first run
├── main.py                 ← UPDATED: Added initialization code
└── ... (other files)
```

---

## ✅ Verification Checklist

After deployment, verify:
- [ ] App loads without errors
- [ ] Login page appears
- [ ] Demo credentials work
- [ ] Can view stock data
- [ ] Can make trades
- [ ] Portfolio updates correctly
- [ ] Wallet balance persists

---

## 🔄 Redeploying After Changes

To redeploy your app after making changes:

1. **Commit and push to GitHub:**
   ```bash
   git add -A
   git commit -m "Your changes here"
   git push origin main
   ```

2. **Trigger redeploy:**
   - Render automatically redeploys on new pushes
   - Or click **"Manual Deploy"** in Render dashboard

3. **Monitor the deployment:**
   - Check the **Logs** tab for any errors
   - Wait for "Build Successful" message

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy/streamlit-cloud)
- [Python Environment Variables](https://12factor.net/config)

---

## 🆘 Need Help?

If you encounter issues:

1. **Check Render Logs** - Most informative for debugging
2. **Verify Environment Variables** - Ensure all are set correctly
3. **Test Locally** - Make sure app works with `streamlit run main.py`
4. **Review Error Messages** - Check app's error details for hints

Good luck! Your Trading App should now work perfectly on Render! 🚀
