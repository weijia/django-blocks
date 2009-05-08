from django.conf.urls.defaults import *
#from blocks.rpc import request
from django.conf import settings
from django.contrib.sitemaps import GenericSitemap
from django.contrib.admin import site

from blocks.apps.core.models import StaticPage


urlpatterns = []

if hasattr(settings, 'BLOCKS_BLOG_URL'):
    urlpatterns += patterns('', (r'^%s/' % settings.BLOCKS_BLOG_URL.strip('/'), include('blocks.apps.blog.urls')), )
                           
if hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
    urlpatterns += patterns('', (r'^%s/' % settings.BLOCKS_AGGREGATOR_URL.strip('/'), include('blocks.apps.aggregator.urls')), )

sitemaps = {}

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
    
    # the sitemap and robots
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps} ),
    (r'^robots.txt$',  'blocks.apps.core.views.robots' ),
)
