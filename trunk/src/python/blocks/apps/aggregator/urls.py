from django.conf.urls.defaults import *
from blocks.apps.aggregator.models import FeedItem

urlpatterns = patterns('blocks.apps.aggregator.views',
    url(r'^$', 'feed_list', None, "feed-list"),
    url(r'^(?P<feed_id>\d+)/$', 'feed_list', None, "feed-detail"),
    url(r'^(?P<feed_id>\d+)/(?P<item_id>\d+)/$', 'feed_detail', None, "feed-item-detail"),
)