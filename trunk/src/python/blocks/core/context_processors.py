def media(request):
    return {'BLOCKS_URL': request.get_full_path()}