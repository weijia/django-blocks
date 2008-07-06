from blocks.core.utils import fix_url, get_menu_title

def media(request):
    url = ''
    bits = fix_url(request.get_full_path()).split('/')
    
    if len(bits) > 2:
        url = fix_url(bits[1])
    else:
        url = '/'
    
    title = get_menu_title(bits[1])
    
    return {'BLOCKS_URL': url, 'BLOCKS_TITLE': title}
