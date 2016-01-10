import os
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ilgiallorosso.net']

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'community',
    'blog',
    'watson'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../templates')],
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

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': conf['general']['db']['name'],
        'USER': conf['general']['db']['username'],
        'PASSWORD': conf['general']['db']['password'],
        'HOST': conf['general']['db']['host'],
        'PORT': ''
    }
}

# AWS CONFIGURATION
AWS_ACCESS_KEY = conf['aws']['accesskey']
AWS_SECRET_KEY = conf['aws']['secretkey']
AWS_STORAGE_STATIC_BUCKET_NAME = conf['aws']['static-bucket']
AWS_STORAGE_MEDIA_BUCKET_NAME = conf['aws']['media-bucket']
AWS_STATIC_DOMAIN = 's3-us-west-2.amazonaws.com/{0}'.format(AWS_STORAGE_STATIC_BUCKET_NAME)
AWS_MEDIA_DOMAIN = 's3-us-west-2.amazonaws.com/{0}'.format(AWS_STORAGE_MEDIA_BUCKET_NAME)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = 'https://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_STATIC_BUCKET_NAME)
STATICFILES_STORAGE = 'ilGiallorosso.custom_storages.CustomStaticStorage'


# MEDIA CONFIGURATION
MEDIA_URL = 'https://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_MEDIA_BUCKET_NAME)
MEDIA_ROOT = os.path.join(BASE_DIR, '../media/ ')
DEFAULT_FILE_STORAGE = 'ilGiallorosso.custom_storages.CustomMediaStorage'

# IS DEV INSTANCE
DEBUG = True