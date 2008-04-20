from django.conf.urls.defaults import *
from django.conf import settings

# putting here the initialization code is ugly but works for now 
import initialization

urlpatterns = patterns('blocks.views',
	(r'^$', 'core.homepage'),
	(r'^home/', 'core.homepage'),
	
	(r'^downloads/', 'core.homepage'),
	(r'^gallery/', 'core.homepage'),
	(r'^docs/', 'core.homepage'),
)

