from django.conf.urls.defaults import *
from blocks.apps.core.views import staticpage
from django.conf import settings
    
urlpatterns = patterns('',
    (r'^%s/' % settings.BLOCKS_BLOG_URL.strip('/'), include('blocks.apps.blog.urls')),
    (r'^%s/' % settings.BLOCKS_AGGREGATOR_URL.strip('/'), include('blocks.apps.aggregator.urls')),              
    (r'^(?P<url>.*)$', staticpage),
)