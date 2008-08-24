from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from django.contrib.comments.feeds import LatestFreeCommentsFeed
from django.contrib.comments.models import FreeComment

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

comments_info_dict = {
    'queryset': FreeComment.objects.filter(is_public=True),
    'paginate_by': 15,
}

feeds = { 'rss': LatestFreeCommentsFeed, }

admin.autodiscover()

urlpatterns += patterns('',
	(r'^admin/(.*)', admin.site.root),

    (r'^blog/', include('blocks.apps.blog.urls')),
	(r'^feeds/', include('blocks.apps.aggregator.urls')),
	
	url(r'^comments/$', 'django.views.generic.list_detail.object_list', comments_info_dict, 'comments-list'),
	(r'^comments/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
   
	(r'', include('blocks.apps.core.urls')),
)
