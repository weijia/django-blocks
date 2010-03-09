from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch

# threadlocals middleware
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)
    
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
    from blocks.apps.core.models import MenuItem
    
    title = url
    
    url = fix_url(url)
    lst = MenuItem.objects.filter(url__exact=url).exclude(name='')
    if (lst):
        trans = getattr(lst[0], 'translation', None)
        if trans:
            title = trans.caption
        else:
            title = lst[0].name
    
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
    if url.startswith('http://') or url.startswith('https://'):
        return url;        
    if not url.startswith('/'):
        url = "/" + url
    if not url.endswith('/'):
        url = url + "/"
    return url

def fix_locale_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url;
    
    if 'localeurl' in settings.INSTALLED_APPS:
        if not url.endswith('/'):
            url = url + "/"
        url = '/'.join(url.split('/')[2:-1])
    
    return fix_url(url)

import sgmllib, string

class StrippingParser(sgmllib.SGMLParser):

    # These are the HTML tags that we will remove
    invalid_tags = ('script', 'style', 'iframe', 'object')

    from htmlentitydefs import entitydefs # replace entitydefs from sgmllib
    
    def __init__(self, invalid_tags=None):
        sgmllib.SGMLParser.__init__(self)
        self.result = ""
        self.endTagList = [] 
        if invalid_tags:
            self.invalid_tags = invalid_tags
        
    def handle_data(self, data):
        if data:
            self.result = self.result + data

    def handle_charref(self, name):
        self.result = "%s&#%s;" % (self.result, name)
        
    def handle_entityref(self, name):
        if self.entitydefs.has_key(name): 
            x = ';'
        else:
            # this breaks unstandard entities that end with ';'
            x = ''
        self.result = "%s&%s%s" % (self.result, name, x)
    
    def unknown_starttag(self, tag, attrs):
        """ Delete all tags except for legal ones """
        if tag not in self.invalid_tags:       
            self.result = self.result + '<' + tag
            for k, v in attrs:
                if string.lower(k[0:2]) != 'on' and string.lower(v[0:10]) != 'javascript':
                    self.result = '%s %s="%s"' % (self.result, k, v)
            endTag = '</%s>' % tag
            self.endTagList.insert(0, endTag)    
            self.result = self.result + '>'
                
    def unknown_endtag(self, tag):
        if tag not in self.invalid_tags:
            self.result = "%s</%s>" % (self.result, tag)
            remTag = '</%s>' % tag
            try:
            	self.endTagList.remove(remTag)
            except:
            	pass

    def cleanup(self):
        """ Append missing closing tags """
        for j in range(len(self.endTagList)):
            self.result = self.result + self.endTagList[j]    
        

def strip_tags(s, invalid_tags=None):
    """ Strip illegal HTML tags from string s """
    parser = StrippingParser(invalid_tags)
    parser.feed(s)
    parser.close()
    parser.cleanup()
    return parser.result

def strip_html(html):
    import re
    return re.sub(r'<[^>]+>', '', html)

def get_related_obj(md):
    related_names = [obj.get_accessor_name() for obj in md._meta.get_all_related_objects()]
    for name in related_names:
        try:
            return getattr(md, name)
        except:
            pass
    return None

def get_related_objs(qs):
    return [get_related_obj(it) for it in qs]
