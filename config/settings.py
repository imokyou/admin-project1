# coding=utf-8
"""
Django settings for mytest project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rygww@y)o746e!_z3y17ck4z!0dxq2kt11z@60o6dmxl24s^wn'

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
    'django_extensions',
    'django_crontab',
    'captcha',
    'dbmodel',
    'app'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.set_lang_middleware.SetLangMiddle'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'template'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
DATABASE_ROUTERS = ['config.db_routers.Router']

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DEFAULT_USER = 'root'
DEFAULT_PSW = 'lupin2008cn'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 3306
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zibenguodu',
        'USER': DEFAULT_USER,
        'PASSWORD': DEFAULT_PSW,
        'HOST': DEFAULT_HOST,
        'PORT': DEFAULT_PORT,
    },
    'zibenguodu': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zibenguodu',
        'USER': DEFAULT_USER,
        'PASSWORD': DEFAULT_PSW,
        'HOST': DEFAULT_HOST,
        'PORT': DEFAULT_PORT,
    }
}

REDIS = {
    'default': {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

SITE_URL = 'http://ziben.js101.local/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     STATIC_ROOT,
# ]

BACKEND_INDEX = '/backend/'
LOGIN_URL = '/backend/login/'

CKEDITOR_UPLOAD_PATH = "/uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 'auto',
    },
}

REDACTOR_OPTIONS = {
    'lang': 'en',
    'minHeight': 400,
}
REDACTOR_UPLOAD = 'uploads/'
REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.UUIDUploader'
REDACTOR_AUTH_DECORATOR = 'django.contrib.auth.decorators.login_required'

CRONJOBS = [
    ('* * */1 * *', 'django.core.management.call_command', ['static_refresh'], {}, '> /tmp/static_refresh.log'),
    ('*/30 * * * *', 'django.core.management.call_command', ['online_refresh'], {}, '> /tmp/online_refresh.log'),
    ('* 3 * * *', 'django.core.management.call_command', ['close_hall'], {}, '> /tmp/close_hall.log'),
]

# 充值相关
CURRENCY_RATIO = 7
PAYMENT_API = 'https://www.95epay.cn/sslpayment'
PAYMENT_RETURNURL = 'http://ziben.js101.local/member/payment-callback/'
PAYMENT_NOTIFYURL = 'http://ziben.js101.local/member/payment-notify/'
# PAYMENT_MERNO = 184647
# PAYMENT_KEY = '_((LToML'

PAYMENT_MERNO = '168885'
PAYMENT_KEY = '12345678'


# django_simple_captcha 验证码配置
# 格式
CAPTCHA_OUTPUT_FORMAT = u'%(text_field)s %(hidden_field)s %(image)s'
# 噪点样式
CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_null',
    # 'captcha.helpers.noise_arcs',
    # 'captcha.helpers.noise_dots',
)

# 图片大小
CAPTCHA_IMAGE_SIZE = (100, 25)
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_LENGTH = 4
CAPTCHA_TIMEOUT = 2


SEND_EMAIL_MAILGUN = True
MAILGUN_MESSAGE_URL = 'https://api.mailgun.net/v3/js101.us/messages'
MAILGUN_API = 'key-9cd9e8c978d5d4836c637202ae0b39d7'
EMAIL_HOST = 'notification@zibenguodu.com'
