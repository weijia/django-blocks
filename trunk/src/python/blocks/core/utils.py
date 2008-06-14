from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch

def get_project_name():
    return settings.SETTINGS_MODULE.split('.')[0]
    
def get_url(view_name, args=None, default=''):
    try:
        return reverse(view_name, args=args)
    except NoReverseMatch:
        try:
            return reverse(get_project_name() + '.' + view_name, args=args)
        except NoReverseMatch:
            return default

def fix_url(url):
    if not url.startswith('/'):
        url = "/" + url
    if not url.endswith('/'):
        url = url + "/"
    return url