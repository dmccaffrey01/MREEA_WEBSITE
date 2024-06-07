"""
Django settings for dj_project project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from celery.schedules import crontab
if os.path.isfile('env.py'):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEVELOPMENT' in os.environ

ALLOWED_HOSTS = ['mreea.org', 'http://www.mreea.org', '70.32.23.32', 'http://70.32.23.32/~mreeaor1/', 'localhost', '127.0.0.1', 'https://mreea-test-568f4c6ab8fc.herokuapp.com/', 'mreea-test-568f4c6ab8fc.herokuapp.com', 'https://test-mreea-website.onrender.com/', 'test-mreea-website.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'home',
    'events',
    'members',
    'contact',
    'profiles',
    'membership',
    'resources',
    'notifications',
    'announcements',
    'storages',
    'blog',
    'django_celery_beat',
    'django_celery_results',
    'ckeditor',
    'ckeditor_uploader',
]

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_SESSION_REMEMBER = False

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

ACCOUNT_FORMS = {
    'signup': 'profiles.forms.CustomSignupForm',
    'change_password': 'profiles.forms.CustomPasswordChangeForm',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
SITE_DOMAIN = 'mreea.org'

POPUP_MESSAGE_TEMPLATE = 'popup_message.html'

LOGIN_REDIRECT_URL = '/profile/login_redirect/' 
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
ACCOUNT_SIGNUP_REDIRECT_URL = '/membership/redirect'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'dj_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'profiles.contexts.profile',
                'membership.contexts.membership_context',
                'notifications.contexts.notifications',
                'notifications.contexts.custom_messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}   


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if DEBUG:
    AWS_STORAGE_BUCKET_NAME = 'mreea-static-files'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_FILE_OVERWRITE = False

    # Additional S3 settings
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None

    # Static files settings
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

    # Media files settings
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # CKEditor settings
    CKEDITOR_UPLOAD_PATH = "blog_images/"
    CKEDITOR_IMAGE_BACKEND = "pillow"
    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': 'full',
            'height': 300,
            'width': '100%',
            'filebrowserUploadUrl': '/ckeditor/upload/',
            'filebrowserBrowseUrl': '/ckeditor/browse/',
        },
    }
else:
    # Local development settings
    CKEDITOR_UPLOAD_PATH = "uploads/"
    CKEDITOR_IMAGE_BACKEND = "pillow"
    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': 'full',
            'height': 300,
            'width': '100%',
            'filebrowserUploadUrl': '/ckeditor/upload/',
            'filebrowserBrowseUrl': '/ckeditor/browse/',
        },
    }


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Add this line to enable TLS
EMAIL_HOST_USER = os.environ.get('HOST_USERNAME')
DEFAULT_FROM_EMAIL = os.environ.get('HOST_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('HOST_EMAIL_PASSWORD')


# REDIS Configuration

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_TIMEZONE = 'America/New_York'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True

CELERY_BEAT_SCHEDULE = {
    'check-membership-task': {
        'task': 'membership.tasks.check_memberships',
        'schedule': crontab(hour=6, minute=0),
    },
}

