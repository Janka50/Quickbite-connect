"""
QuickBite Connect - Production Settings
"""
from .base import *
import dj_database_url

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}


# Database - use dj_database_url to parse DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Add this for Render
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Static files on Render
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

print("🚀 Running in PRODUCTION mode")