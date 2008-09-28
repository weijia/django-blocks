from django.conf.urls.defaults import *
from blocks.apps.aggregator.feeds import LatestEntries
from blocks.apps.aggregator.views import list, feed_list, detail

feeds = {'rss': LatestEntries, }

urlpatterns = patterns('',
    url(r'^$', list, name="aggregator.list"),
    url(r'^(?P<feed_id>\d+)/$', feed_list, name="aggregator.feedlist"),
    url(r'^(?P<feed_id>\d+)/(?P<item_id>\d+)/$', detail, name="aggregator.detail"),
    
    (r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)