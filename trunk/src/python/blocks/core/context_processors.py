from blocks.core.utils import fix_url, get_menu_title
from django.conf import settings

def media(request):
    url = ''
    bits = fix_url(request.get_full_path()).split('/')
    
    if len(bits) > 2:
        url = fix_url(bits[1])
    else:
        url = '/'
    
    title = get_menu_title(bits[1])

    context = {
        'BLOCKS_URL': url,
        'BLOCKS_FULL_URL': request.get_full_path(),
        'BLOCKS_TITLE': title,
        'BLOCKS_LANGUAGES': settings.BLOCKS_LANGUAGES,
        'BLOCKS_USELANG': settings.BLOCKS_USELANG,
    }
    
    if hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
        context['BLOCKS_AGGREGATOR_URL'] = settings.BLOCKS_AGGREGATOR_URL

    if hasattr(settings, 'BLOCKS_BLOG_URL'):
        context['BLOCKS_BLOG_URL'] = settings.BLOCKS_BLOG_URL
    
    return context
