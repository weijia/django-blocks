import os
from django.conf import settings

if not settings.TEMPLATE_DIRS:
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)