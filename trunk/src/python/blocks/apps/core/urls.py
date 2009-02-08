from django.conf.urls.defaults import *
from blocks.rpc import request
from django.conf import settings

urlpatterns = []

if hasattr(settings, 'BLOCKS_BLOG_URL'):
    urlpatterns += patterns('', (r'^%s/' % settings.BLOCKS_BLOG_URL.strip('/'), include('blocks.apps.blog.urls')), )
                           
if hasattr(settings, 'BLOCKS_AGGREGATOR_URL'):
    urlpatterns += patterns('', (r'^%s/' % settings.BLOCKS_AGGREGATOR_URL.strip('/'), include('blocks.apps.aggregator.urls')), )

urlpatterns += patterns('',
    (r'^json/', request.rpc_request),
)
