# Django settings for loco project.

import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Kimus Linuxus', 'kimus.linuxus@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "../db/private.db")


TIME_ZONE = 'Europe/Lisbon'
LANGUAGE_CODE = 'en-us'
USE_I18N = False

SITE_ID = 1

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates")
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_z9v#(dwasd$w0a-asda&r8d^w2_savxykqc#0p)%hbd*+j@$ylr+z#o'

ROOT_URLCONF = 'personal.urls'

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.CacheMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'blocks.core.context_processors.media'
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.admin',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
#    'django.contrib.sites',
	
    'blocks.apps.contenttypes',
    'blocks.apps.admin',
	'blocks.apps.wiki',
    'blocks.apps.aggregator',
)

#CACHE_BACKEND = 'locmem:///'
#CACHE_MIDDLEWARE_SECONDS = 60 * 5 # 5 minutes

class NullStream(object):
    def write(*args, **kwdargs):
        pass
    writeline = write
    writelines = write
        
RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'doctitle_xform': False,
    'cloak_email_addresses': True,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'warning_stream': NullStream()
}
