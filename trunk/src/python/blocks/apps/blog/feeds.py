from django.contrib.syndication.feeds import Feed
from blocks.apps.blog import models
from blocks.core import utils
from django.conf import settings

class LatestEntries(Feed):
	title = "latest blog entries"
	link = utils.get_url('feed-list', None, settings.BLOCKS_BLOG_URL) + 'rss/'
	description = "Latest blog entries list"

	def items(self):
		return models.BlogEntry.objects.order_by('-modified_date')[:10]
