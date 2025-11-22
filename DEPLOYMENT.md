# Deployment Guide for QR Code Attendance System

## ⚠️ Important: Netlify Limitation

**Netlify is NOT suitable for Flask applications.** Netlify is designed for static sites and serverless functions, while Flask requires a persistent server process.

## ✅ Recommended Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

1. **Sign up** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select "Web Service"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: Python 3

3. **Set Environment Variables:**
   - `SECRET_KEY` - Generate a strong secret key
   - `DATABASE_URL` - Your MySQL connection string
     - Format: `mysql+pymysql://admin:admin%40123@192.168.137.60/qrattendance`
   - Or use Render's PostgreSQL (free tier available)

4. **Deploy:**
   - Render will automatically deploy on git push

### Option 2: Railway.app (Free Tier Available)

1. **Sign up** at [railway.app](https://railway.app)

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure:**
   - Railway will auto-detect Python
   - Add environment variables:
     - `SECRET_KEY`
     - `DATABASE_URL`
   - Railway will use the `Procfile` automatically

4. **Deploy:**
   - Railway auto-deploys on push

### Option 3: Heroku (Paid, but reliable)

1. **Install Heroku CLI** from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create App:**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=mysql+pymysql://admin:admin%40123@192.168.137.60/qrattendance
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 4: PythonAnywhere (Free Tier Available)

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your code** via Git or upload files

3. **Configure Web App:**
   - Set source code directory
   - Set WSGI file to point to your app
   - Add environment variables in Web tab

4. **Configure MySQL:**
   - Use PythonAnywhere's MySQL or connect to external MySQL

## 🔧 Pre-Deployment Checklist

1. **Update `config.py`** to use environment variables:
   ```python
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Ensure database is accessible** from the deployment server (update firewall rules if needed)

3. **Update `app.py`** to use production settings:
   ```python
   if __name__ == '__main__':
       app.run(debug=False, host='0.0.0.0', port=5000)
   ```

4. **Test locally** with production-like settings:
   ```bash
   gunicorn app:app
   ```

## 🌐 Environment Variables Needed

```bash
SECRET_KEY=your-strong-secret-key-here
DATABASE_URL=mysql+pymysql://admin:admin%40123@192.168.137.60/qrattendance
QR_EXPIRY_MINUTES=120
LECTURE_HALL_RADIUS=100
```

## 📝 Database Access

**Important:** Your MySQL server at `192.168.137.60` must be:
- Accessible from the internet (if deploying to cloud)
- OR use a cloud database service (Render PostgreSQL, Railway MySQL, etc.)
- Firewall configured to allow connections from deployment server

## 🚀 Quick Deploy to Render

1. Push code to GitHub
2. Go to render.com → New → Web Service
3. Connect GitHub repo
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add environment variables
6. Deploy!

## 🔒 Security Notes for Production

1. Change default admin password
2. Use strong SECRET_KEY
3. Use HTTPS (most platforms provide this automatically)
4. Configure proper CORS if needed
5. Use environment variables for sensitive data
6. Regularly backup database

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Heroku Docs: https://devcenter.heroku.com

