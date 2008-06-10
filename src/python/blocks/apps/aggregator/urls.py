from django.conf.urls.defaults import *
from blocks.apps.aggregator.feeds import LatestEntries

feeds = {'rss': LatestEntries, }

urlpatterns = patterns('',
    url(r'^$', 'blocks.apps.aggregator.views.feed_list', None, "feed-list"),
    url(r'^(?P<feed_id>\d+)/$', 'blocks.apps.aggregator.views.feed_list', None, "feed-detail"),
    url(r'^(?P<feed_id>\d+)/(?P<item_id>\d+)/$', 'blocks.apps.aggregator.views.feed_detail', None, "feed-item-detail"),
    
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)