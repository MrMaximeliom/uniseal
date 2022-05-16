
import os
from datetime import timedelta
from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='qpxw@svn0mi40y_mzt5&l((_9vwynu5vv0u)r($y_gv)')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost','uniseal-api.herokuapp.com','93.188.162.130','13-244-177-56']
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
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'uniseal',
#         'USER': 'root',
#         'PASSWORD': '1a79a001973e92c89aa42c0c9c8a8bf3e138132bc81bad4a5e03a8b908b1e317',
#         'HOST': '13.245.16.122',
#         'PORT': '5432',
#     }
# }
# Heroku DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4nnvv8lb1aedj',
        'USER': 'gkvvbjmricafua',
        'PASSWORD': '1a79a001973e92c89aa42c0c9c8a8bf3e138132bc81bad4a5e03a8b908b1e317',
        'HOST': 'ec2-52-23-40-80.compute-1.amazonaws.com',
        'PORT': '5432',
    }
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

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'unisealAPI.authentication.UnisealAuthentication',


    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

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