from blocks.core.utils import fix_url    

def media(request):
    bits = fix_url(request.get_full_path()).split('/')
    if len(bits) > 2:
        url = fix_url(bits[1])
    else:
        url = '/'
    return {'BLOCKS_URL': url}
