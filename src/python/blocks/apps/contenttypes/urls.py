from django.conf.urls.defaults import *

urlpatterns = patterns('blocks.apps.contenttypes.views',
    (r'^(?P<url>.*)$', 'staticpage'),
)