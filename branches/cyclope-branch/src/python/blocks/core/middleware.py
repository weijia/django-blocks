from blocks.apps.core.views import staticpage
from blocks.core.utils import _thread_locals
from django.http import Http404
from django.conf import settings

class CommonMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)
    
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a staticpage for non-404 responses.
        try:
            return staticpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
