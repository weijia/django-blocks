from django.conf.urls.defaults import *

urlpatterns = patterns('blocks.apps.core.views',
    (r'^(?P<url>.*)$', 'staticpage'),
)