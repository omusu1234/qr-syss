# 🚀 Quick Deployment Guide

## ⚠️ Netlify Won't Work!

**Netlify doesn't support Flask applications.** Use one of these instead:

## ✅ Easiest: Render.com (5 minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in:
   - **Name:** qr-attendance
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click "Advanced" and add Environment Variables:
   ```
   SECRET_KEY = (generate a random string)
   DATABASE_URL = mysql+pymysql://admin:admin%40123@192.168.137.60/qrattendance
   ```
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Done! Your app will be live at `your-app.onrender.com`

## 🔧 Important: Database Access

Your MySQL server at `192.168.137.60` needs to be:
- ✅ Accessible from the internet (if deploying to cloud)
- ✅ Firewall configured to allow external connections
- ✅ OR use a cloud database service (recommended)

### Better Option: Use Cloud Database
1. **Render PostgreSQL** (free tier):
   - Create PostgreSQL database on Render
   - Update `DATABASE_URL` to use PostgreSQL connection string
   - Update `requirements.txt` to use `psycopg2-binary` instead of `PyMySQL`

2. **Railway MySQL** (free tier):
   - Create MySQL database on Railway
   - Use provided connection string

## 📝 Environment Variables

Add these in your deployment platform:

```bash
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=mysql+pymysql://admin:admin%40123@192.168.137.60/qrattendance
QR_EXPIRY_MINUTES=120
LECTURE_HALL_RADIUS=100
```

## 🎯 Alternative: Railway.app (Also Free)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Add environment variables (same as above)
5. Railway auto-detects Python and uses `Procfile`
6. Deploy!

## 🔍 Test Locally First

Before deploying, test with production server:

```bash
pip install gunicorn
gunicorn app:app
```

Visit `http://localhost:8000` to test.

## 📞 Need Help?

- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app
- **Heroku:** https://devcenter.heroku.com

