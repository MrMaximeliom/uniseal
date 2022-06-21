
import os
from datetime import timedelta
from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='qpxw@svn0mi40y_mzt5&l((_9vwynu5vv0u)r($y_gv)')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=True, cast=bool)
DEBUG = True

ALLOWED_HOSTS = [config("INTERNAL_HOST"),config("HEROKU_HOST"),config("AWS_HOST")]
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.accounts',
    'apps.brochures',
    'apps.product',
    'apps.project',
    'apps.sellingPoint',
    'apps.supplier',
    'apps.category',
    'apps.solution',
    'apps.admin_panel',
    'apps.slider',
    'apps.dashboard',
    'django_filters',
    'apps.address',
    'mathfilters',
    'apps.notifications',
    'apps.sms_notifications',
    'apps.approvals',
    'crispy_forms',
    'apps.company_info',
    'apps.project_application',
    'apps.industry_updates',
    'apps.handle_errors',
    'apps.application_videos',
    'apps.orders',
    'apps.jop_type',
    'apps.offer',
    'apps.common_code',
    'apps.request_permissions'
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
AUTH_USER_MODEL = 'accounts.User'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'unisealAPI.urls'
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

WSGI_APPLICATION = 'unisealAPI.wsgi.application'
# AWS DATABASE
# Paused for development purposes will be back after development is completed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("AWS_DB_NAME"),
        'USER': config("AWS_DB_USER"),
        'PASSWORD': config("AWS_PASSWORD"),
        'HOST': config("AWS_HOST"),
        'PORT': config("AWS_PORT"),
    }
}
# # Heroku DATABASE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config("HEROKU_DB_NAME"),
#         'USER': config("HEROKU_DB_USER"),
#         'PASSWORD': config("HEROKU_PASSWORD"),
#         'HOST': config("HEROKU_HOST"),
#         'PORT': config("HEROKU_PORT"),
#     }
# }
# RDS DATABASE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config("RDS_DB_NAME"),
#         'USER':  config("RDS_DB_USER"),
#         'PASSWORD':  config("RDS_PASSWORD"),
#         'HOST':  config("RDS_HOST"),
#         'PORT':  config("RDS_PORT"),
#     }
# }
# # temporary database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

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

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':3,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'unisealAPI.authentication.UnisealAuthentication',


    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],



}
CACHES = {
    'default':{
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Khartoum'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))