from django.contrib.syndication.feeds import Feed
from django.utils.translation import ugettext_lazy as _
from demo.apps.news.models import NewsArticle

class NewsFeed(Feed):
	title = _("News Articles")
	link = '/rss/news/'
	description = _("LINUX.PT News Articles list")

	def items(self):
		return NewsArticle.objects.published()[:10]
