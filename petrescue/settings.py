"""
Django settings for PetRescue project.

This project helps connect lost pets with their owners and facilitates pet adoptions.
It provides a platform for reporting lost/found pets, searching for missing animals,
and supporting animal welfare through donations.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def env_list(name, default=''):
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(',') if item.strip()]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret.
LOCAL_SECRET_KEY = 'django-insecure-local-dev-only-change-me'
SECRET_KEY = os.environ.get('SECRET_KEY', LOCAL_SECRET_KEY)

# SECURITY WARNING: Don't run with debug turned on in production.
DEBUG = env_bool('DEBUG', default=True)

if not DEBUG and SECRET_KEY == LOCAL_SECRET_KEY:
    raise ImproperlyConfigured('SECRET_KEY must be set when DEBUG=False.')

# Hosts allowed to access the application.
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', default='localhost,127.0.0.1')


# Application definition
# List of Django applications installed in this project

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    
    # Custom applications
    'main',  # Main application containing core functionality
]

# Middleware components that process requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'petrescue.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'main' / 'templates'],  # Template directories
        'APP_DIRS': True,  # Automatically discover templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application entry point
WSGI_APPLICATION = 'petrescue.wsgi.application'


# Database configuration
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')
DB_NAME = os.environ.get('DB_NAME')

if DB_ENGINE == 'django.db.backends.sqlite3':
    DB_NAME = DB_NAME or str(BASE_DIR / 'db.sqlite3')
else:
    DB_NAME = DB_NAME or 'petrescue_db'

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
    }
}

if DB_ENGINE != 'django.db.backends.sqlite3':
    DATABASES['default'].update({
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    })

    if not DEBUG:
        required_db_settings = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
        missing_db_settings = [
            setting for setting in required_db_settings
            if not os.environ.get(setting)
        ]
        if missing_db_settings:
            missing = ', '.join(missing_db_settings)
            raise ImproperlyConfigured(
                f'{missing} must be set when DEBUG=False and using a non-SQLite database.'
            )


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
# Enforcing strong password policies for user security

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
# Configuration for language and timezone settings

LANGUAGE_CODE = 'en-us'  # Default language for the application

TIME_ZONE = 'UTC'  # Timezone for the application

USE_I18N = True  # Enable internationalization

USE_TZ = True  # Enable timezone support


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# Configuration for serving static assets like CSS, JS, and images

STATIC_URL = 'static/'  # URL prefix for static files

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Directory containing static files
]

# Media files (user-uploaded content)
# Directory where user-uploaded files will be stored
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
# Using BigAutoField for better performance with large datasets

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
# Using our custom User model instead of Django's default
AUTH_USER_MODEL = 'main.User'

# Authentication URLs
# Redirect URLs for login/logout actions
LOGIN_URL = '/login/'  # URL for login page
LOGIN_REDIRECT_URL = '/'  # Redirect after successful login
LOGOUT_REDIRECT_URL = '/login/'  # Redirect after logout
