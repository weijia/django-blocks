from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from blocks.apps.core.core_models import BaseContentModel
from blocks.apps.core.managers import BaseManager

from tagging.fields import TagField
from tagging.models import Tag


class BlogEntry(BaseContentModel):
	slug = models.SlugField()
	comments_enabled = models.BooleanField(_('comments enabled'), default=True, help_text=_("enable comments for this entry"))	
	tag_list = TagField(_('tag list'), help_text=_('tags for this entry'))
	
	objects = BaseManager()
	
	def _get_tags(self):
		return Tag.objects.get_for_object(self)
	def _set_tags(self, tag_list):
		Tag.objects.update_tags(self, tag_list)
	tags = property(_get_tags, _set_tags)

	def __unicode__(self):
		return self.name
	
	def get_absolute_url(self):
		year = self.publish_date.strftime("%Y").lower()
		month = self.publish_date.strftime("%m").lower()
		day = self.publish_date.strftime("%d").lower()
		return "%s%s/%s/%s/%s/" % (settings.BLOCKS_BLOG_URL, year, month, day, self.slug)
	
	class Meta:
		db_table = 'blogentry'
		verbose_name_plural = _('Blog Entries')
		ordering = ('-publish_date',)
		get_latest_by = 'publish_date'


class BlogEntryTranslation(models.Model):
	article = models.ForeignKey(BlogEntry, related_name="translations")
	language  = models.CharField(max_length=25, choices=settings.BLOCKS_LANGUAGES, editable=True)
	
	title = models.CharField(_('title'), max_length=200)
	lead = models.TextField(_('lead'), max_length=255)
	body = models.TextField(_('body'))
	
	def __unicode__(self):
		return u'%s: %s' % (self.article, self.language)
	
	class Meta:
		db_table = 'blogentry_translation'
		ordering = ["id"] # sets up default ordering by language
		verbose_name = _('Blog Entry Translation')
		verbose_name_plural = _('Blog Entry Translations')