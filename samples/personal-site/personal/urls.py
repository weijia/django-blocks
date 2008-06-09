from django.conf.urls.defaults import *
#from django.contrib import admin
from django.conf import settings

urlpatterns = []

if settings.MEDIA_URL.startswith('/'):
	media_url = settings.MEDIA_URL
	if media_url.startswith('/'):
	   media_url = media_url[1:]
	if media_url.endswith('/'):
	   media_url = media_url[:-1]
	urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % (media_url), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
	#(r'^admin/(.*)', admin.site.root),
	(r'^admin/', include('django.contrib.admin.urls')),

	(r'^feeds/', include('blocks.apps.aggregator.urls')),
	(r'', include('blocks.apps.contenttypes.urls')),
)
