from blocks.core.utils import fix_url, fix_locale_url, get_menu_title
from django.conf import settings

def media(request):
    url = ''
    full_url = fix_locale_url(request.get_full_path())
    bits = full_url.split('/')
    
    if len(bits) > 2:
        url = bits[1]
    else:
        url = '/'

    context = {
        'BLOCKS_URL': fix_url(url),
        'BLOCKS_FULL_URL': full_url,
        'BLOCKS_TITLE': get_menu_title(url),
        'BLOCKS_FULL_TITLE': get_menu_title(full_url),
        'BLOCKS_LANGUAGES': settings.BLOCKS_LANGUAGES,
        'BLOCKS_USELANG': settings.BLOCKS_USELANG,
        'BLOCKS_SETTINGS': settings,
    }
    
    if hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
        context['BLOCKS_AGGREGATOR_URL'] = settings.BLOCKS_AGGREGATOR_URL

    if hasattr(settings, 'BLOCKS_BLOG_URL'):
        context['BLOCKS_BLOG_URL'] = settings.BLOCKS_BLOG_URL
    
    return context
