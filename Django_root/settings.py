"""
Django settings for Django_root project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from config._0_config import (SECRET_KEY,
ALLOWED_HOSTS,
COOKIE_TIME,
LINE_CHANNEL_ACCESS_TOKEN,
LINE_CHANNEL_SECRET )

# +---------------------+
# | Directory Structure |
# +---------------------+
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # 專案 根目錄
APP_DIR = os.path.join(BASE_DIR, "apps")                                        # app 根目錄                               
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")                              # templates 根目錄
STATIC_DIR = os.path.join(BASE_DIR, "static")                                   # static 根目錄
MEDIA_DIR = os.path.join(BASE_DIR, "media")                                     # media 根目錄



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.line_bot',
    'apps.web_site',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
 
ROOT_URLCONF = 'Django_root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # let templates use {{ MEDIA_URL }}
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Django_root.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_L10N = True

# USE_TZ = True


# SESSION settings
SESSION_COOKIE_AGE = COOKIE_TIME        # change expired session (3 hours)      <default 2 weeks>
SESSION_SAVE_EVERY_REQUEST = False      # save session every request            <default False>
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # keep login even browser close         <default False>
# SESSION_COOKIE_SECURE = False         # pass cookie through HTTPs
# SESSION_COOKIE_HTTPONLY = True        # HTTP only                             <default True>
# SESSION_COOKIE_NAME == "sessionid"    # session cookie in client browser key



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_FINDERS = [
   'django.contrib.staticfiles.finders.FileSystemFinder',
   'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = 'C:\\Users\\admin\\gsld\\line_bot_test\\movie_line\\static'
    
STATICFILES_DIRS = [STATIC_DIR, ]
STATIC_URL = '/static/'
COMPRESS_ENABLED=True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')+'/' # 'data' is my media folder
# MEDIA_URL = '/media/'


LINE_CHANNEL_ACCESS_TOKEN = LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET = LINE_CHANNEL_SECRET


if 'dyno' in os.environ:
    DEBUG = True
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)