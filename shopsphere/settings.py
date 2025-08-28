from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-dz)qh^-iqyn7fo@_h=mix)n9^+^9lcg_ajli@h6d62^h%kg#*z"
DEBUG = True

ALLOWED_HOSTS = [
  "apis.shopsphere.midoghanam.site",
  "localhost",
  "127.0.0.1",
  "130.61.206.180",
  "ec2-13-53-53-248.eu-north-1.compute.amazonaws.com"
  
]

CSRF_TRUSTED_ORIGINS = [
  "https://localhost:8000",
  "http://127.0.0.1",
  "http://130.61.206.180",
  "https://apis.shopsphere.midoghanam.site",
]

#CORS_ALLOWED_ORIGINS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', 
    'django.contrib.messages', "corsheaders",
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework', 'rest_framework_simplejwt',
    "authentication", "core", "administrators",
    "clients",
    
]

## Django Rest Framework Settings
SIMPLE_JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
  "ROTATE_REFRESH_TOKENS": True,
  "BLACKLIST_AFTER_ROTATION": True,
  "AUTH_HEADER_TYPES": ("Bearer",),
}

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
  'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
}

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.locale.LocaleMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  "corsheaders.middleware.CorsMiddleware",
  "django.middleware.common.CommonMiddleware",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'rate-limit-cache',
  }
}

ROOT_URLCONF = 'shopsphere.urls'

TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',],},},]

WSGI_APPLICATION = 'shopsphere.wsgi.application'

DATABASE_ROUTERS = ['shopsphere.routers.DbRouter']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dbs/db.sqlite3',
    },
    'core': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dbs/core.db',
    },
    "main": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "dbs/main.db",
    },
}

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', }, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },]
LOGIN_URL = '/auth/login/'

LOGOUT_URL = '/auth/logout/'

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
  ('en', 'English'),
]

LANGUAGE_CODE = 'en'
USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
