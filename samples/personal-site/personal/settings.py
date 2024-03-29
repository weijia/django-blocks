# Django settings for loco project.

import os.path

APPEND_SLASH = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Kimus Linuxus', 'kimus.linuxus@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "../db/private.db")


TIME_ZONE = 'Europe/Lisbon'
LANGUAGE_CODE = 'en'
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
	'django.middleware.cache.CacheMiddleware',
	'django.middleware.http.SetRemoteAddrFromForwardedFor',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
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
	'blocks.apps.core',
	'blocks.apps.administration',
	'blocks.apps.blog',
	'blocks.apps.aggregator',
	'blocks.apps.comments',
	
	'django.contrib.auth',
	'django.contrib.admin',
	'django.contrib.comments',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.humanize',

	'tagging',
)

#CACHE_BACKEND = 'locmem:///'
#CACHE_MIDDLEWARE_SECONDS = 60 * 5 # 5 minutes

class NullStream(object):
	def write(*args, **kwdargs):
		pass
	writeline = write
	writelines = write
		
RESTRUCTUREDTEXT_FILTER_SETTINGS = {
	'doctitle_xform': True,
	'initial_header_level': 2,
	'cloak_email_addresses': True,
	'file_insertion_enabled': False,
	'raw_enabled': False,
	'warning_stream': NullStream()
}

DEFAULT_FROM_EMAIL = 'Django-Blocks Administrator <some.email@server.net>'
EMAIL_HOST = 'pop.server.net'
EMAIL_HOST_USER = 'popuser'
EMAIL_HOST_PASSWORD = 'poppwd'
