import os
from django.conf import settings

if not hasattr(settings, 'TEMPLATE_DIRS'):
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

if not hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
    settings.BLOCKS_AGGREGATOR_URL = '/feeds/'
