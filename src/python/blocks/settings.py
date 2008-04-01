import os

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
TIME_ZONE = 'America/Chicago'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "media")
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
TEMPLATE_DIRS = [os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
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
)

CACHE_MIDDLEWARE_SECONDS = 1 #60 * 5 # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'djangoblocks'
CACHE_MIDDLEWARE_GZIP = True
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

BLOCKS_MEDIA_SERVE = True