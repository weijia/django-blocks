from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers

from blocks.apps.core import core_models
from blocks.apps.core.managers import BaseManager
from demo.apps.site.models import *

#
# News Article
#
class NewsArticle(ArticleModel):
	"""
	Primary NewsArticle info object: does not itself contain translations
	"""
	date = models.DateField(_('date'))
	local = models.CharField(_('local'), max_length=200, null=True, blank=True)
	image = forms.BlocksImageField(_('image'), upload_to='images', sizes=[('thumbnail', 100, 86), ('detail', 254, 160),], null=True, blank=True)

	objects = BaseManager()

	def __unicode__(self):
		return u'%s (%s)' % (self.name, self.date)

	def get_absolute_url(self):
		return urlresolvers.reverse('demo.apps.news.views.detail', kwargs={'item_id': self.id })

	class Meta:
		db_table = 'news_article'
		verbose_name = _('News Article')
		verbose_name_plural = _('News Articles')
		ordering = ('-date',)


class NewsArticleTranslation(models.Model):
	"""
	NewsArticle content translation - language-based
	"""

	article = models.ForeignKey(NewsArticle, related_name="translations")
	language  = models.CharField(max_length=25, choices=settings.BLOCKS_LANGUAGES, editable=True)

	title = models.CharField(_('title'), max_length=200)
	date_desc = models.CharField(_('date description'), max_length=200, null=True, blank=True)
	lead  = models.TextField(_('lead'), max_length=500)
	text  = models.TextField(_('text'), max_length=64000)

	def __unicode__(self):
		return u'%s: %s' % (self.article, self.language)

	class Meta:
		db_table = 'news_article_translation'
		ordering = ["id"] # sets up default ordering by language
		verbose_name = _('News Article Translation')
		verbose_name_plural = _('News Article Translations')
