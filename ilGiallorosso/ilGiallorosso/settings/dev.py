import os
from .base import *

ALLOWED_HOSTS = ['www.noticiasroma.com', 'dev.noticiasroma.com']

DEBUG = True

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'community',
    'fifastats',
    'blog',
    'watson',
    'boto',
    'storages',
    'autocomplete_light',
    'debug_toolbar',
    'compressor',
    'django_jinja',
    # 'awesome_gallery',
)

SITE_ID = 1

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'TIMEOUT': 60,
        'LOCATION': '10.0.0.239:6379',
    },
}

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'ilGiallorosso.timezoneMiddleware.TimezoneMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 'django.template.context_processors.tz',
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
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, '../templates/jinja')],
        "APP_DIRS": True,
        "OPTIONS": {
        	'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # Match the template names ending in .html but not the ones in the admin folder.
            "match_extension": ".html",
            "match_regex": r"^(?!admin/).*",
            "app_dirname": "templates",

            # Can be set to "jinja2.Undefined" or any other subclass.
            "undefined": None,

            "newstyle_gettext": True,
            # "tests": {
            #     "mytest": "path.to.my.test",
            # },
            # "filters": {
            #     "myfilter": "path.to.my.filter",
            # },
            # "globals": {
            #     "myglobal": "path.to.my.globalfunc",
            # },
            # "constants": {
            #     "foo": "bar",
            # },
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
                'compressor.contrib.jinja2ext.CompressorExtension',
            ],
            "bytecode_cache": {
                "name": "default",
                "backend": "django_jinja.cache.BytecodeCache",
                "enabled": False,
            },
            "autoescape": True,
            "auto_reload": DEBUG,
            "translation_engine": "django.utils.translation",
        }
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
        'PORT': '5432'
    }
}

# AWS CONFIGURATION
AWS_ACCESS_KEY_ID = conf['aws']['accesskey']
AWS_SECRET_ACCESS_KEY = conf['aws']['secretkey']
AWS_STORAGE_STATIC_BUCKET_NAME = conf['aws']['static-bucket']
AWS_STORAGE_MEDIA_BUCKET_NAME = conf['aws']['media-bucket']
AWS_STATIC_DOMAIN = 's3-us-west-2.amazonaws.com/{0}'.format(AWS_STORAGE_STATIC_BUCKET_NAME)
AWS_MEDIA_DOMAIN = 's3-us-west-2.amazonaws.com/{0}'.format(AWS_STORAGE_MEDIA_BUCKET_NAME)
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False

from django.utils import timezone

expires = timezone.now() + timezone.timedelta(days=5)

AWS_HEADERS = {
    'Expires': expires.strftime('%a, %d %b %Y 20:00:00 GMT'),
    'Cache-Control': 'max-age=86400',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = 'http://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_STATIC_BUCKET_NAME)
STATICFILES_STORAGE = 'ilGiallorosso.custom_storages.CustomStaticStorage'

# django-compressor conf
COMPRESS_ENABLED = True
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = os.path.join(BASE_DIR, '../static/')
AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_STATIC_BUCKET_NAME


# MEDIA CONFIGURATION
MEDIA_URL = 'https://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_MEDIA_BUCKET_NAME)
MEDIA_ROOT = os.path.join(BASE_DIR, '../media/ ')
DEFAULT_FILE_STORAGE = 'ilGiallorosso.custom_storages.CustomMediaStorage'

# AWESOME GALLERY CONFIGS
AWESOME_LANGUAGES_ALERTS = 'ES'
AWESOME_APP_BLOG_NAME = 'blog'
AWESOME_APP_MODEL_TAG = 'Tag'
AWESOME_GALLERY_PAGINATOR_ELEMENTS = 10
AWESOME_GALLERY_SEARCH_BY_TAGS_TEMPLATE = 'elements_by_tags'
AWESOME_GALLERY_GALLERY_TEMPLATE = 'gallery'
AWESOME_GALLERY_GALERIES_TEMPLATE = 'galeries'
AWESOME_GALLERY_SIZES = ((50, 50), (100, 100), (470, 350), (670, 495), (780, 480), (1024, 800))

#DEBUG_TOOLBAR_PATCH_SETTINGS = False
# IS DEV INSTANCE
IS_MOBILE = False
# INTERNAL_IPS = ('127.0.0.1','52.71.227.216',)

# def custom_show_toolbar(self):
#     return True

# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': True,
#     'ENABLE_STACKTRACES' : True,
#     'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
# }

