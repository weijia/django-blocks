import os
from django.conf import settings

settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)