from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

#from django.contrib.comments.feeds import LatestFreeCommentsFeed
#from django.contrib.comments.models import FreeComment

urlpatterns = []

# only serve static files if in a debug enviorment and the media url is relative
if settings.MEDIA_URL.startswith('/') and settings.DEBUG == True:
	media_url = settings.MEDIA_URL.strip('/')
	urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % (media_url), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

#comments_info_dict = {
#    'queryset': FreeComment.objects.filter(is_public=True),
#    'paginate_by': 15,
#}

#feeds = { 'rss': LatestFreeCommentsFeed, }

admin.autodiscover()

urlpatterns += patterns('',
	(r'^admin/(.*)', admin.site.root),

    (r'^blog/', include('blocks.apps.blog.urls')),
	(r'^feeds/', include('blocks.apps.aggregator.urls')),
	
	(r'^comments/', include('django.contrib.comments.urls')),
	   
	(r'', include('blocks.apps.core.urls')),
)
