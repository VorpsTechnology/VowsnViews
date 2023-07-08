
from pathlib import Path

import os
from .local_settings import *

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = Secret_key


# DEBUG = False
DEBUG = True
ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ['vowsnviews.com', 'www.vowsnviews.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Site name is admin

    # Install apps
    'crispy_forms',  # Crispy forms
    'import_export',  # Excel import export for products and category and csv
    'widget_tweaks',  # Filters Widget
    'django_filters',  # Filters
    'ckeditor',  # Rich Text Editor

    # Django apps
    'analytics.apps.AnalyticsConfig',
    'listing_analytics.apps.ListingAnalyticsConfig',
    'home.apps.HomeConfig',
    'order.apps.OrderConfig',
    'products.apps.ProductsConfig',
    'users.apps.UsersConfig',
    'listing.apps.VendorListingConfig',
    'vendors.apps.VendorsConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vowsnviews.urls'

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
                'order.context_processors.cart_list',  # show cart in all page
                'analytics.context_processors.analytics_data',  # show order in analytics page
                'home.context_processors.currency_form',  # currency form and news letter
                'home.context_processors.header_data',  # header data
                'home.context_processors.save_user_location',
                'home.context_processors.get_current_year_to_context',
                'vendors.context_processors.get_notifications',# CY

            ],
        },
    },
]

WSGI_APPLICATION = 'vowsnviews.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "vowsnvie_siteguide",
#         "USER": "siteguide_amit",
#         "PASSWORD": data_base_pass,
#         "HOST": "localhost",
#         "PORT": "3306",
#     }
# }


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
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


SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Calcutta'  # Indian time
USE_I18N = True
USE_L10N = True
USE_TZ = True

# User Model
AUTH_USER_MODEL = 'users.User'  # Custom User Model

# BootStrap
CRISPY_TEMPLATE_PACK = 'bootstrap4'  # To use Bootstrap

#Basic Static and Media Files settings
# STATIC_URL = '/static/'
# STATIC_ROOT = '/home/vowsnvie/public_html/static'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = '/home/vowsnvie/public_html/media'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'home'  # Redirect after login
LOGIN_URL = 'users-login'  # Login URL
LOGOUT_URL = 'users-login'  # Logout URL

# SSL
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Basic Email sending settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = Email 
EMAIL_HOST_PASSWORD = Email_Pass
