from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
#from django.core.xheaders import populate_xheaders

DEFAULT_TEMPLATE = 'blocks/default.html'

def staticpage(request, url):
    from blocks.apps.core.models import StaticPage
    from django.conf import settings

    
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url

    p = StaticPage.objects.published(request)
    f = None

    # check if there's a exact match first
    try:
        f = p.get(url__exact=url)
    except StaticPage.DoesNotExist:
        if settings.BLOCKS_SP_REDIRECT:
            # try and get relative pages first
            try:
                f = p.filter(menu__exact=url)[:1].get()
                return HttpResponseRedirect(f.url)
            except StaticPage.DoesNotExist:
                pass
            
            # try to get
            try:
                from blocks.apps.core.models import MenuItem
                menu = MenuItem.objects.get(url=url)
                if menu:
                    return HttpResponseRedirect(menu.children()[0].url)
            except:
                raise Http404('No Static Page matches the given query.')
        raise Http404('No Static Page matches the given query.')
    
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    #if f.registration_required and not request.user.is_authenticated():
    #    from django.contrib.auth.views import redirect_to_login
    #    return redirect_to_login(request.path)
    if f.template:
        t = loader.select_template((f.template.template, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    c = RequestContext(request, {'page': f,  'object': f})

    response = HttpResponse(t.render(c))
    #populate_xheaders(request, response, StaticPage, f.id)
    return response
