from django.contrib.syndication.feeds import Feed
from blocks.apps.aggregator import models
from blocks.core import utils
from django.conf import settings

class LatestEntries(Feed):
    title = "latest feeds"
    link = utils.get_url('feed-list', None, settings.BLOCKS_AGGREGATOR_URL) + 'rss/'
    description = "Latest feed list"

    def items(self):
        return models.FeedItem.objects.order_by('-date_modified')[:10]
