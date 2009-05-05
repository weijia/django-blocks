from blocks.core.utils import fix_url, get_menu_title
from django.conf import settings

def media(request):
    url = ''
    bits = fix_url(request.get_full_path()).split('/')
    
    if len(bits) > 2:
        url = fix_url(bits[1])
    else:
        url = '/'

    context = {
        'BLOCKS_URL': url,
        'BLOCKS_FULL_URL': request.get_full_path(),
        'BLOCKS_TITLE': get_menu_title(bits[1]),
        'BLOCKS_FULL_TITLE': get_menu_title(request.get_full_path()),
        'BLOCKS_LANGUAGES': settings.BLOCKS_LANGUAGES,
        'BLOCKS_USELANG': settings.BLOCKS_USELANG,
        'BLOCKS_SETTINGS': settings,
    }
    
    if hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
        context['BLOCKS_AGGREGATOR_URL'] = settings.BLOCKS_AGGREGATOR_URL

    if hasattr(settings, 'BLOCKS_BLOG_URL'):
        context['BLOCKS_BLOG_URL'] = settings.BLOCKS_BLOG_URL
    
    return context
