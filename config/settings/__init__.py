import os
from decouple import config

ENVIRONMENT = config('DJANGO_ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *

print(f"⚙️  Loaded settings for: {ENVIRONMENT.upper()}")