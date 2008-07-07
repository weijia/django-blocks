from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.xheaders import populate_xheaders

from blocks.apps.core.models import StaticPage

DEFAULT_TEMPLATE = 'default.html'

def staticpage(request, url):
    from blocks.core.utils import fix_url
    url = fix_url(url)
        
    f = get_object_or_404(StaticPage, url__exact=url)
    
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    #if f.registration_required and not request.user.is_authenticated():
    #    from django.contrib.auth.views import redirect_to_login
    #    return redirect_to_login(request.path)
    if f.template:
        t = loader.select_template((f.template.template, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    c = RequestContext(request, {'page': f, })
    
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, StaticPage, f.id)
    return response