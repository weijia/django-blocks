from django.contrib.syndication.feeds import Feed
from blocks.apps.aggregator import models
from blocks.core import utils

class LatestEntries(Feed):
    title = "latest feeds"
    link = utils.get_url('feed-list', None, '/feeds/') + 'rss/'
    description = "Latest feed list"

    def items(self):
        return models.FeedItem.objects.order_by('-date_modified')[:10]
