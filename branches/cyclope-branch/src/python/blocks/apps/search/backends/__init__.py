import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

__all__ = ['backend']

if not hasattr(settings, "BLOCKS_SEARCH_ENGINE"):
    raise ImproperlyConfigured("You must define the BLOCKS_SEARCH_ENGINE setting before using the search framework.")

class_name = "%sBackend" % settings.BLOCKS_SEARCH_ENGINE.split(".")[-1].capitalize()
try:
    # Most of the time, the search backend will be one of the  
    # backends that ships with django-search, so look there first.
    mod = __import__('blocks.apps.search.backends.%sbe' % settings.BLOCKS_SEARCH_ENGINE, {}, {}, class_name)
    backend = getattr(mod, class_name)
except ImportError, e:
    raise
    # If the import failed, we might be looking for a search backend 
    # distributed external to django-search. So we'll try that next.
    try:
        mod = __import__(settings.BLOCKS_SEARCH_ENGINE, {}, {}, class_name)
        backend = getattr(mod, class_name)
    except ImportError, e_user:
        # The database backend wasn't found. Display a helpful error message
        # listing all possible (built-in) database backends.
        backend_dir = __import__('blocks.apps.search.backends', {}, {}, ['']).__path__[0]
        available_backends = [
            os.path.splitext(f)[0] for f in os.listdir(backend_dir)
            if f != "base.py"
            and not f.startswith('_') 
            and not f.startswith('.') 
            and not f.endswith('.pyc')
        ]
        available_backends.sort()
        if settings.BLOCKS_SEARCH_ENGINE not in available_backends:
            raise ImproperlyConfigured, "%r isn't an available search backend. Available options are: %s" % \
                (settings.BLOCKS_SEARCH_ENGINE, ", ".join(map(repr, available_backends)))
        else:
            raise # If there's some other error, this must be an error in Django itself.