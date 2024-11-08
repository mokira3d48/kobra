"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import logging
import logging.config
from pathlib import Path
from dotenv import load_dotenv


# loads the configs from .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Logging config
logging.config.fileConfig(BASE_DIR / 'logging.conf')
logging.getLogger(__name__).info("Loading setting ...")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(gxw3-6s!-&b#hv*-dg2j=ub%tyd21^!n-s*w6+18&g6obwf@n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # `*` is used to allowed all host.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Settings of list of domains that cant access to ressources
# of yours server.
# CORS_ALLOWED_ORIGINS = [];
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# REST framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # several authentication classes are used.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    # Pagination system settings for all API view that returns a data list.
    # In this case, the size of a page is set to 8.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 16,

    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'EXCEPTION_HANDLER': 'core.exceptions.exception_handler_fn',

    # Configure size of uploaded files (bytes).
    # 'FILE_UPLOAD_MAX_MEMORY_SIZE': 120 * 1024 * 1024,  # 120MB
    'DATA_UPLOAD_MAX_MEMORY_SIZE': 120 * 1024 * 1024,  # 120MB
}

# Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Kobra APIs Documentation',
    'DESCRIPTION': (
			'Kobra project for using to create server program.'
		),
    'VERSION': '1.0.0',
    'COMPONENT_SPLIT_REQUEST': True,
    'SERVE_INCLUDE_SCHEMA': False,
    "LOGIN_URL": "/admin/login/",  # URL of login to API documentation.
    "LOGOUT_URL": "/admin/logout/",  # URL of logout from API documentation.
}


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Settings of a basic database with PostgreSQL.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv("DB_NAME", ''),
#         'USER': os.getenv("USERNAME", ''),
#         'PASSWORD': os.getenv("PASSWORD", ''),
#         'HOST': os.getenv("HOST", ''),
#         'PORT': os.getenv('PORT', ''),
#     }
# }

# Settings of a spacial database with PostgreSQL.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('USERNAME'),
#         'PASSWORD': os.getenv('PASSWORD'),
#         'HOST': os.getenv('HOST'),
#         'PORT': os.getenv('PORT'),
#     },
# }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Path to traduction files
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # '/var/www/static/',
]

# Base url to serve media files
MEDIA_URL = '/file/'
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FILE UPLOADING:
# -----------------------------------------------------------------------------
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 120

# Maximal size of an uploaded file in bytes (default 2.5MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 128 * 1024 * 1024  # 128MB

# Maximal total size of uploaded files in one request (default 2.5MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 256 * 1024 * 1024  # 256MB


# SESSION SETTINGS:
# -----------------------------------------------------------------------------
# Duration of session expiration:
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week (value is in second)

# Make end session when client browser closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
