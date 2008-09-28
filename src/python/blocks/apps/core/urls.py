from django.conf.urls.defaults import *
from blocks.apps.core.views import staticpage

urlpatterns = patterns('',                       
    (r'^(?P<url>.*)$', staticpage),
)