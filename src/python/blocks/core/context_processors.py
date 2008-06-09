def media(request):
    bits = request.get_full_path().split('/')
    if len(bits) > 2:
        url = bits[1]
    else:
        url = 'home'
    return {'BLOCKS_URL': url}
