from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^r/', include('django.conf.urls.shortcut')),
)

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
	(r'^admin/', include('django.contrib.admin.urls')),
	(r'', include('blocks.apps.core.urls')),
)
