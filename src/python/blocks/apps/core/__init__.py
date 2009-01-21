import os
from django.conf import settings

if not hasattr(settings, 'TEMPLATE_DIRS'):
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

settings.BLOCKS_LANGUAGES = settings.LANGUAGES if settings.USE_I18N else [it for it in settings.LANGUAGES if it[0] == settings.LANGUAGE_CODE]
settings.BLOCKS_USELANG = settings.USE_I18N