"""
Django settings for carblog project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.utils.translation import gettext_lazy as _
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w8u9kg$5f8lv)@-ec=fuoorerjk@c@w#x#$s+vtxr0nnzelp=n'
# для разработки нижнюю строку закоммент, верхнюю разкоммент.
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'w8u9kg$5f8lv)@-ec=fuoorerjk@c@w#x#$s+vtxr0nnzelp=n')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# для разработки нижнюю строку закоммент, верхнюю разкоммент.
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'markupsafe',
    'blog_engine',
    'tinymce',
    'treebeard',
    'parler',
    'sorl.thumbnail',
    'rosetta',
    'rest_framework',
    'api',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'pagination.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'carblog.urls'

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     'DIRS': ['%s/blog_engine/jinjatemplates/'% (PROJECT_DIR),
    #              os.path.join(BASE_DIR, "jinjatemplates")],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'environment': 'blog_engine.myjinja2.JinjaEnvironment'
    #     }
    # },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'blog_engine/templates')],
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

TEMPLATE_CONTEXT_PROCESSORS = [
    # "django.core.context_processors.auth",
    # "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    # "django.core.context_processors.media",
    "django.core.context_processors.request"
]

WSGI_APPLICATION = 'carblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# настройки мультиязычности сайта
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uk', _('Ukraine')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

# настройки django-parler
PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'ru'},
        {'code': 'uk'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False, # не скрывать то, что перевести не удалось
    }
}

# настройка для кеширования

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "d:/rve_work/carblog_cache/",
    }
}

#end настройка для кеширования

# end настройки мультиязычности сайта

# настройки django rest framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# end настройки django rest framework


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'blog_engine/files')
MEDIA_URL = '/blog_engine/files/'

# настройки для отправки почты
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "paradoxtestsoft@gmail.com"
EMAIL_HOST_PASSWORD = "testingprogram"
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# конец настроек для отправки почты


# это была попытка использовать rabbitmq
CELERY_BROKER_URL = 'amqp://localhost'

BROKER_URL = 'amqp://paradox:paradox@localhost:5672/paradox_host'


# Activate Django-Heroku.
django_heroku.settings(locals())


