# this file maybe be replaced by blocks.core.db_settings module that will store
# all manageble settings in the database and call the settings.configure().
# see: http://www.djangoproject.com/documentation/settings/#using-settings-without-setting-django-settings-module
# of course that DATABASE settings need to be here.

import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Kimus Linuxus', 'kimus.linuxus@gmail.com'),)
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'kimus.linuxus@gmail.com'
EMAIL_SUBJECT_PREFIX = "[Blocks]"

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "db/blocks.db")

SITE_ID = 1
USE_I18N = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Lisbon'

# src/python/blocks => src/
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_PATH, "media")
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
TEMPLATE_DIRS = [os.path.join(ROOT_PATH, "templates")]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'blocks.core.context_processors.media',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.http.SetRemoteAddrFromForwardedFor',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.cache.CacheMiddleware',
)

ROOT_URLCONF = 'blocks.urls'

INSTALLED_APPS = (
#	'django.contrib.sites',
	'django.contrib.auth',
	'django.contrib.admin',
#	'django.contrib.comments',
	'django.contrib.contenttypes',
#	'django.contrib.flatpages',
	'django.contrib.humanize',
#	'django.contrib.redirects',
	'django.contrib.sessions',
	'django.contrib.sitemaps',
	
	# blocks applications
	'blocks.apps.core',
    'blocks.apps.contenttypes',
)

CACHE_MIDDLEWARE_SECONDS = 1 #60 * 5 # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'djangoblocks'
CACHE_MIDDLEWARE_GZIP = True
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

BLOCKS_MEDIA_SERVE = True
BLOCKS_LOGGING_FILE = os.path.join(os.path.dirname(__file__), "db/blocks.log")