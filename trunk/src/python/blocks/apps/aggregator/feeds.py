from django.contrib.syndication.feeds import Feed
from blocks.apps.aggregator import models

class LatestEntries(Feed):
    title = "latest feeds"
    link = "/feeds/rss/"
    description = "Latest feed list"

    def items(self):
        return models.FeedItem.objects.order_by('-date_modified')[:10]
