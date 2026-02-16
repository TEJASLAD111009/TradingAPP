# Trading App - Deployment Guide

Complete guide to deploy the Trading App to various platforms.

## 📋 Pre-Deployment Checklist

- [ ] All files present and correct
- [ ] Dependencies in requirements.txt
- [ ] Virtual environment tested locally
- [ ] App runs without errors: `streamlit run main.py`
- [ ] Demo credentials work
- [ ] Stock data fetches correctly
- [ ] Portfolio/Wallet operations tested
- [ ] README and STRUCTURE docs updated

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (RECOMMENDED - FREE)

**Easiest & Best for Streamlit Apps**

#### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Trading App"
git remote add origin https://github.com/YOUR_USERNAME/trading.git
git push -u origin main
```

#### Step 2: Deploy on Streamlit Cloud
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your GitHub repo
4. Select:
   - Repository: `your-username/trading`
   - Branch: `main`
   - File: `main.py`
5. Click "Deploy"

#### Step 3: Share Your App
- Streamlit generates a unique URL
- Share with others: `https://share.streamlit.io/...`
- No server maintenance needed!

**Pros:**
- ✅ Free tier available
- ✅ Automatic updates from GitHub
- ✅ Built-in scaling
- ✅ No configuration needed
- ✅ Custom domain support (paid)

**Cons:**
- ❌ May sleep if no activity
- ❌ Limited to Streamlit ecosystem

---

### Option 2: Heroku (PAID - $7+/month)

**Traditional PaaS Deployment**

#### Step 1: Create Heroku Account
- Sign up at [heroku.com](https://www.heroku.com)
- Install Heroku CLI

#### Step 2: Create Procfile
```bash
# In project root
echo "web: streamlit run main.py --logger.level=error" > Procfile
```

#### Step 3: Create requirements.txt
```bash
# Already done in the project
```

#### Step 4: Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

#### Step 5: View Logs
```bash
heroku logs --tail
```

**Pros:**
- ✅ Full control over environment
- ✅ Custom domains
- ✅ Always running
- ✅ Good reliability

**Cons:**
- ❌ Paid service ($7-50/month)
- ❌ More complex setup
- ❌ Needs maintenance

---

### Option 3: Docker Containerization

**Deploy Anywhere with Docker**

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Create .dockerignore
```
__pycache__
.git
.gitignore
venv/
.env
data/
*.pyc
```

#### Step 3: Build Docker Image
```bash
docker build -t trading-app .
```

#### Step 4: Run Locally
```bash
docker run -p 8501:8501 trading-app
```

#### Step 5: Push to Docker Hub (Optional)
```bash
docker tag trading-app YOUR_DOCKER_USERNAME/trading-app
docker push YOUR_DOCKER_USERNAME/trading-app
```

**Deployment Targets:**
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean
- Any Kubernetes cluster

---

### Option 4: AWS (FREE TIER Available)

#### Using AWS EC2
```bash
# 1. Create EC2 instance (Ubuntu)
# 2. SSH into instance
ssh -i key.pem ubuntu@your-ec2-ip

# 3. Install Python
sudo apt update
sudo apt install python3-pip python3-venv -y

# 4. Clone repo
git clone https://github.com/YOUR_USERNAME/trading.git
cd trading

# 5. Create venv and install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Run with nohup
nohup streamlit run main.py --server.port 80 &

# 7. Access at http://your-ec2-ip
```

#### Using AWS Lambda + API Gateway (Advanced)
- Requires AWS-specific framework
- More complex setup
- Best for REST API, not Streamlit

**Pros:**
- ✅ FREE tier (1 year)
- ✅ Scalable
- ✅ Always running

**Cons:**
- ❌ Requires AWS knowledge
- ❌ More setup needed
- ❌ Paid after free tier

---

### Option 5: Google Cloud Platform

#### Using Cloud Run (Simplest)
```bash
# 1. Create Google Cloud account
# 2. Install gcloud CLI

# 3. Authenticate
gcloud auth login

# 4. Create project
gcloud projects create trading-app

# 5. Deploy with gcloud
gcloud run deploy trading-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Pros:**
- ✅ Generous FREE tier (180,000 vCPU/month)
- ✅ Auto-scaling
- ✅ Easy deployment
- ✅ Pay-per-use

**Cons:**
- ❌ Scales down when idle
- ❌ Google account needed

---

### Option 6: DigitalOcean (RECOMMENDED for VPS)

#### Simple VPS Deployment
```bash
# 1. Create DigitalOcean account
# 2. Create Droplet (Ubuntu $5/month)

# 3. SSH into droplet
ssh root@your-droplet-ip

# 4. Setup application
apt update && apt upgrade -y
apt install python3-pip python3-venv git -y

# 5. Clone and setup
git clone https://github.com/YOUR_USERNAME/trading.git
cd trading
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Setup Supervisor (process manager)
apt install supervisor -y

# Create /etc/supervisor/conf.d/trading.conf
[program:trading]
command=/root/trading/venv/bin/streamlit run /root/trading/main.py --server.port 8501
directory=/root/trading
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/trading.err.log
stdout_logfile=/var/log/trading.out.log

# 7. Enable and start
supervisorctl reread
supervisorctl update
supervisorctl start trading

# 8. Setup Nginx reverse proxy
# (Point port 80 to 8501)
```

**Pros:**
- ✅ Affordable ($5-40/month)
- ✅ Always running
- ✅ Full control
- ✅ Easy management

**Cons:**
- ❌ Need some Linux knowledge
- ❌ Basic server maintenance required

---

### Option 7: Your Own Server/Laptop (Development)

#### Background Process on Windows
```bash
# Run in background
python -m streamlit run main.py &

# or use new terminal window
start "Trading App" cmd /k "streamlit run main.py"
```

#### Keep Running After Logout (Linux/Mac)
```bash
# Using screen
screen -S trading
streamlit run main.py
# Press Ctrl+A then D to detach

# Reattach
screen -r trading

# Or use nohup
nohup streamlit run main.py > app.log 2>&1 &
```

---

## 🔧 Post-Deployment Tasks

### 1. Database Migration (Optional but Recommended)
```python
# Add this to models for PostgreSQL support
import psycopg2
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/trading_db')
```

### 2. Set Up SSL/HTTPS
- Use Let's Encrypt (free)
- Configure web server (Nginx/Apache)
- Redirect HTTP to HTTPS

### 3. Environment Variables
```bash
# .env file (don't commit to git)
DATABASE_URL=your_database_url
STOCK_API_KEY=optional_api_key
SECRET_KEY=your_secret_key
```

### 4. Monitoring & Logging
```bash
# Monitor app health
curl https://your-app.com
```

### 5. Backup Strategy
- Regular JSON file backups
- Or database backups if using SQL
- Cloud storage (S3, Google Drive)

### 6. SSL Certificate (Recommended)
```bash
# Using Let's Encrypt with Certbot
sudo certbot certonly --standalone -d yourdomain.com
```

---

## 📊 Performance Tips

### For All Deployments:
1. **Cache Stock Prices**
   - Update every 5 minutes instead of per-request
   - Use Redis for caching

2. **Optimize Database Queries**
   - Add indexes to frequently queried fields
   - Use connection pooling

3. **Reduce API Calls**
   - Batch fetch multiple stocks
   - Cache results for 1 hour

4. **CDN for Static Assets**
   - Images, CSS, JS served from CDN
   - Faster load times

### Streamlit-Specific:
```python
# Add to main.py
import streamlit as st

@st.cache_resource
def load_stock_data():
    return get_popular_stocks()

data = load_stock_data()  # Cached!
```

---

## 🆘 Deployment Troubleshooting

### Issue: App crashes on deploy
**Solution:** Check logs, ensure all dependencies in requirements.txt

### Issue: Port 8501 not accessible
**Solution:** Configure firewall, use port 80, setup reverse proxy

### Issue: Out of memory
**Solution:** Implement caching, pagination, database optimization

### Issue: High latency
**Solution:** Upgrade server, add caching layer, use CDN

### Issue: Stock API rate limited
**Solution:** Implement cache, use different API, upgrade YFinance

---

## 🎯 Deployment Recommendation by Use Case

| Scenario | Recommended | Why |
|----------|------------|-----|
| **Personal Project** | Local/Streamlit Cloud | Free, easy |
| **Small Business** | DigitalOcean VPS | Affordable, reliable |
| **Production App** | AWS/GCP | Scalable, professional |
| **Learning/Demo** | Streamlit Cloud | Instantly deployed |
| **Multiple Environments** | Docker | Consistent across platforms |

---

## 🔐 Security Checklist

- [ ] Passwords hashed (SHA-256 or better)
- [ ] HTTPS enabled
- [ ] Database credentials in .env
- [ ] API keys not in code
- [ ] CSRF protection if adding forms
- [ ] Input validation on all fields
- [ ] Rate limiting on requests
- [ ] Regular security updates
- [ ] Backup and disaster recovery plan

---

## 📱 Scaling for More Users

1. **Phase 1 (0-100 users):**
   - Single VPS with Streamlit
   - JSON file storage

2. **Phase 2 (100-1000 users):**
   - Upgrade to PostgreSQL
   - Add caching layer (Redis)
   - Separate backend API

3. **Phase 3 (1000+ users):**
   - Kubernetes orchestration
   - Multiple servers
   - Professional monitoring
   - 24/7 support

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/library/get-started/installation)
- [Docker Docs](https://docs.docker.com/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Google Cloud Docs](https://cloud.google.com/docs)

---

**Deployment Guide Version:** 1.0
**Last Updated:** February 2026

Good luck with your deployment! 🚀
