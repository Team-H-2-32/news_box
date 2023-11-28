"""
Django settings for news project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mw0=pzg+!vl^noh5$l-2$g1+fo=z4xfl(#$9!5wgtc9j91*ado'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'user',
    'news_app',
    'main',

    'gevent',
    'modeltranslation'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news.urls'

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

WSGI_APPLICATION = 'news.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES["default"] = dj_database_url.parse("postgres://news_box_db_z285_user:tHWuztNZpmFeiNFPBvviOLOkZc2kt9h7@dpg-cli0p57jc5ks73ep2n90-a.oregon-postgres.render.com/news_box_db_z285")

DATABASES = {
    'default': dj_database_url.parse("postgres://news_box_db_z285_user:tHWuztNZpmFeiNFPBvviOLOkZc2kt9h7@dpg-cli0p57jc5ks73ep2n90-a.oregon-postgres.render.com/news_box_db_z285")
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja-ja'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'user.User'

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_URL = '/user/login/'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = BASE_DIR, 'locale/',

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ("ja", _("Japanese")),
    ("en", _("English")),
    ("ru", _("Russian")),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ja'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Tokyo'
# CELERY_RESULT_BACKEND = 'rpc://'
# broker_connection_retry_on_startup = True
# CELERYD_CONCURRENCY = 'gevent'
# CELERY_BEAT_SCHEDULE = {
#     'get_all_news': {
#         'task': 'news.task.get_all_news',
#         'schedule': crontab(hour='*', minute='0, 15, 30, 45'),
#     },
# }


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '019alisobirov@gmail.com'
EMAIL_HOST_PASSWORD = 'rxxfxdonmucxobbv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False