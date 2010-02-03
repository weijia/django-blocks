import os
from django.conf import settings

if not hasattr(settings, 'BLOCKS_ADMIN_HELP'):
    settings.BLOCKS_ADMIN_HELP = {}

if not hasattr(settings, 'ADMIN_MEDIA_ROOT'):
    settings.ADMIN_MEDIA_ROOT = "%sadmin/" % (settings.MEDIA_URL)

if not hasattr(settings, 'TEMPLATE_DIRS'):
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

if not hasattr(settings, 'BLOCKS_SP_REDIRECT'):
    settings.BLOCKS_SP_REDIRECT = False

if not hasattr(settings, 'BLOCKS_IMAGE_SIZES'):
    settings.BLOCKS_IMAGE_SIZES = [('thumbnail', 96, 96), ('detail', 270, 173), ]

if not hasattr(settings, 'GOOGLE_MAPS_API_KEY'):
    settings.GOOGLE_MAPS_API_KEY = 'NONE'

settings.BLOCKS_LANGUAGES = settings.LANGUAGES if settings.USE_I18N else [it for it in settings.LANGUAGES if it[0] == settings.LANGUAGE_CODE]
settings.BLOCKS_USELANG = (len(settings.BLOCKS_LANGUAGES) > 0)