from django.conf.urls.defaults import *
#from blocks.rpc import request
from django.conf import settings
from django.contrib.sitemaps import GenericSitemap
from django.contrib.admin import site
from django.core import urlresolvers
from django.contrib import admin

from blocks.apps.core.models import StaticPage


urlpatterns = []

# only serve static files if in a debug enviorment and the media url is relative
if settings.MEDIA_URL.startswith('/') and settings.DEBUG == True:
    media_url = settings.MEDIA_URL.strip('/')
    admin_media_url = settings.ADMIN_MEDIA_PREFIX.strip('/')
    urlpatterns += patterns('',
        (r'^%s/blocks/(?P<path>.*)$' % (media_url), 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_ROOT}),
        (r'^%s/(?P<path>.*)$' % (media_url), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'path': 'img/favicon.ico'}),
    )

if hasattr(settings, 'BLOCKS_BLOG_URL'):
    urlpatterns += patterns('', (r'^%s/' % settings.BLOCKS_BLOG_URL.strip('/'), include('blocks.apps.blog.urls')), )
                           
if hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
    urlpatterns += patterns('', (r'^%s/' % settings.BLOCKS_AGGREGATOR_URL.strip('/'), include('blocks.apps.aggregator.urls')), )

if not hasattr(settings, 'FILEBROWSER_URL_ADMIN'):
    settings.FILEBROWSER_URL_ADMIN = '/admin/filebrowser/'

if getattr(settings, 'FILEBROWSER_ENABLED', False):
    urlpatterns += patterns('', (r'^%s/' % settings.FILEBROWSER_URL_ADMIN.strip('/'), include('filebrowser.urls')), )

sitemaps = {}

try:
    admin_url = urlresolvers.reverse('%sadmin_index' % site.name)
except urlresolvers.NoReverseMatch:
    admin_url = '/%s' % site.root_path

for model, model_admin in site._registry.items():
    isok = getattr(model, 'get_absolute_url', None) and getattr(model.objects, 'published', None)
    if isok:
        model_label = model.__name__.lower()
        info_dict = {
            'queryset': model.objects.published(),
            'date_field': 'lastchange_date',
        }    
        sitemaps[model_label] = GenericSitemap(info_dict)

urlpatterns += patterns('',
    #(r'^json/', request.rpc_request),
    
    # menuitem history fix
    (r'^%s/core/menuitem/(?P<item_id>\d+)/$' % admin_url.strip('/'), 'blocks.apps.core.views.menuitem'),
    
    # the sitemap and robots
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps} ),
    (r'^robots.txt$',  'blocks.apps.core.views.robots' ),
    
        
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # administration site
    (r'^admin/', include(admin.site.urls)),
)
