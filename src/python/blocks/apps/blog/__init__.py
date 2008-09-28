import os
from django.conf import settings

try:
    settings.TEMPLATE_DIRS
except AttributeError:
    settings.TEMPLATE_DIRS = []
    
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

try:
    settings.BLOCKS_BLOG_URL
except AttributeError:
    settings.BLOCKS_BLOG_URL = '/blog/'
