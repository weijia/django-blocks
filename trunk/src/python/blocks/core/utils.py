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

def get_menu_title(url):
    from blocks.apps.contenttypes.models import Menu
    
    title = url
    
    url = fix_url(url)
    lst = Menu.objects.filter(url__exact=url)
    if (lst):
        title = lst[0].title
    
    return title
        
def get_page_title(url):
    title = url
    
    url = fix_url(url)
    feed = get_url('feed_list')
    blog = get_url('blog-index')
    
    if (url == feed):
        from blocks.apps.aggregator.models import FeedItem
        pass
    
    elif (url == blog):
        from blocks.apps.blog.models import BlogEntry
        pass
    
    else:
        from blocks.apps.contenttypes.models import StaticPage
        lst = StaticPage.objects.filter(url__exact=url)
        if (lst):
            title = lst[0].title
    
    return title
    
def fix_url(url):
    if not url.startswith('/'):
        url = "/" + url
    if not url.endswith('/'):
        url = url + "/"
    return url