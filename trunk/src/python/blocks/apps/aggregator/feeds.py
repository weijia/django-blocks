from django.contrib.syndication.feeds import Feed
from blocks.apps.aggregator.models import FeedItem
from django.conf import settings

class LatestEntries(Feed):
    title = "latest feeds"
    link = '%srss/'% settings.BLOCKS_AGGREGATOR_URL
    description = "Latest feed list"

    def items(self):
        return FeedItem.objects.order_by('-date_modified')[:10]
