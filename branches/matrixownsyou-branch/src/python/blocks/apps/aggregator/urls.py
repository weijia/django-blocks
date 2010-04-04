from django.conf.urls.defaults import url, patterns
from blocks.apps.aggregator.feeds import LatestEntries

feeds = {'rss': LatestEntries, }

urlpatterns = patterns('blocks.apps.aggregator.views',
	url(r'^$',								   'list',	  name="aggregator.list"),
	url(r'^(?P<feed_id>\d+)/$',				  'feed_list', name="aggregator.feedlist"),
	url(r'^(?P<feed_id>\d+)/(?P<item_id>\d+)/$', 'detail',	name="aggregator.detail"),	
)
urlpatterns += patterns('',
	(r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)