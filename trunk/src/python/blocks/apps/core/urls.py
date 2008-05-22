from django.conf.urls.defaults import *
from django.conf import settings

# putting here the initialization code is ugly but works for now 
from blocks import initialization

urlpatterns = patterns('',
	(r'', include('blocks.apps.contenttypes.urls')),
)

