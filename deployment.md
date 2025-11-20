# 🚀 QuickBite Connect - Deployment Guide

## Deployment to Railway.app

### Prerequisites
- Railway.app account (free tier available)
- GitHub repository (optional but recommended)

### Step 1: Prepare Your Project

1. **Ensure all files are committed to Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub** (optional)
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy to Railway

#### Option A: Deploy from GitHub

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway and select your repository
5. Railway will automatically detect Django and start deployment

#### Option B: Deploy using Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

### Step 3: Add PostgreSQL Database

1. In Railway dashboard, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provision database and set DATABASE_URL

### Step 4: Add Redis (Optional for Caching)

1. In Railway dashboard, click "New"
2. Select "Database" → "Redis"
3. Copy the Redis URL for REDIS_URL environment variable

### Step 5: Configure Environment Variables

In Railway dashboard, go to your service → Variables, add:

```
DJANGO_ENVIRONMENT=production
SECRET_KEY=<generate-a-secure-50-character-key>
ALLOWED_HOSTS=<your-app-name>.railway.app
DEBUG=False

# Database (auto-configured by Railway)
DATABASE_URL=<auto-set-by-railway>

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe
STRIPE_PUBLIC_KEY=pk_live_your_key
STRIPE_SECRET_KEY=sk_live_your_key

# Twilio (Optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Google Maps
GOOGLE_MAPS_API_KEY=your_api_key

# Redis (if added)
REDIS_URL=<redis-connection-url>
CELERY_BROKER_URL=<redis-connection-url>

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Step 6: Run Migrations

After deployment, run migrations:

```bash
railway run python manage.py migrate
```

### Step 7: Create Superuser

```bash
railway run python manage.py createsuperuser
```

### Step 8: Seed Sample Data (Optional)

```bash
railway run python manage.py seed_data
```

### Step 9: Access Your Application

Your app will be available at:
- API: `https://<your-app-name>.railway.app`
- Admin: `https://<your-app-name>.railway.app/admin`
- API Docs: `https://<your-app-name>.railway.app/api/docs/`

---

## Alternative Deployment Options

### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create quickbite-connect
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set DJANGO_ENVIRONMENT=production
   heroku config:set SECRET_KEY=your-secret-key
   # ... add other variables
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

### Deploy to AWS EC2

1. **Launch EC2 Instance** (Ubuntu 22.04)

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip postgresql nginx
   ```

4. **Clone Repository**
   ```bash
   git clone <your-repo>
   cd Quick-bite
   ```

5. **Setup Virtual Environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Configure PostgreSQL**
   ```bash
   sudo -u postgres createdb quickbite_db
   sudo -u postgres createuser quickbite_user
   ```

7. **Setup Gunicorn & Nginx**
   - Create systemd service file
   - Configure Nginx as reverse proxy

8. **Setup SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations completed
- [ ] Superuser created
- [ ] Static files collected
- [ ] SSL/HTTPS enabled
- [ ] CORS origins configured
- [ ] Email service tested
- [ ] Payment gateway tested (test mode)
- [ ] API documentation accessible
- [ ] Error tracking configured (Sentry)
- [ ] Backup strategy in place
- [ ] Monitoring setup
- [ ] Domain configured (if custom domain)

---

## Monitoring & Maintenance

### Health Check
- Monitor: `https://your-app.railway.app/api/health/`

### Logs
```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# AWS
sudo journalctl -u gunicorn
```

### Database Backups
- Railway: Automatic backups included
- Heroku: `heroku pg:backups:capture`
- AWS: Configure automated RDS snapshots

---

## Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Issue: Database connection failed
- Check DATABASE_URL environment variable
- Verify database is running
- Check firewall/security group settings

### Issue: 500 Internal Server Error
- Check logs for detailed error
- Verify all environment variables set
- Ensure SECRET_KEY is set in production

### Issue: CORS errors
- Add frontend domain to CORS_ALLOWED_ORIGINS
- Check CORS middleware is enabled

---

## Security Best Practices

1. **Never commit sensitive data**
   - Use environment variables
   - Keep .env out of version control

2. **Use strong SECRET_KEY**
   - Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

3. **Enable HTTPS only**
   - Set SECURE_SSL_REDIRECT=True in production

4. **Regular updates**
   - Keep dependencies updated
   - Monitor security advisories

5. **Database security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

---

## Support

For deployment issues:
- Check Railway documentation: https://docs.railway.app
- Review Django deployment checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Open an issue on GitHub