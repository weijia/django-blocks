# -*- coding: utf-8 -*-

import os.path

from django.utils.translation import ugettext_lazy as _

## SITE SETTINGS ##


## DATABASE SETTINGS ##

USE_MYSQL = False

if USE_MYSQL:
    DATABASE_ENGINE   = 'mysql'
    DATABASE_NAME     = 'demo'
    DATABASE_USER     = 'someusr'
    DATABASE_PASSWORD = 'somepwd'
    DATABASE_HOST     = 'localhost'

else:
    DATABASE_ENGINE   = 'sqlite3'
    DATABASE_NAME     = os.path.join(os.path.dirname(__file__), "../../db/demo.db").replace('\\','/')
    
## LOCALIZATION SETTINGS ##

TIME_ZONE = 'Europe/Lisbon'
LANGUAGE_CODE = 'pt' # default language
USE_I18N = True

LANGUAGES = (
  ('pt', _('Portuguese')),
  ('en', _('English')),
)



## CACHE SETTINGS ##

#CACHE_BACKEND = 'locmem:///'
#CACHE_MIDDLEWARE_SECONDS = 60 * 5 # 5 minutes


## EMAIL SETTINGS ##

DEFAULT_FROM_EMAIL = 'DEMO <noreply@zlabs.org>'

# testing sercer: python -m smtpd -n -c DebuggingServer localhost:1025

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'


# specifies who should get code error notifications
ADMINS = (
    ('kimus', 'kimus@zlabs.org'),
)

# specifies who should get broken-link notifications when 
MANAGERS = ADMINS


## MISC SETTINGS ##
APPEND_SLASH = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates")
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5jhk&qv&nyu^ot&gk)p(%$65x7k9t)wjvg^d&ukcxv6eh*rxzf'

ROOT_URLCONF = 'demo.urls'

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.CacheMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'blocks.core.middleware.CommonMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    
    'blocks.core.context_processors.media'
)

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.markup',
    
    # django-blocks core applications
    'blocks.apps.core',
    'blocks.apps.administration',

    # django-blocks add-ons applications
    #'blocks.apps.aggregator',
    'blocks.apps.aggregator',

    # django-blocks based applications 
    'demo.apps.site',
    'demo.apps.news',
)

## BLOCKS SETTINGS ##

BLOCKS_SP_REDIRECT = True
BLOCKS_AGGREGATOR_URL = '/feeds/'
#BLOCKS_BLOG_URL = '/blog/'


## PROFILE SETTINGS ##

ACCOUNT_ACTIVATION_DAYS = 3
AUTH_PROFILE_MODULE = 'profiles.UserProfile'
