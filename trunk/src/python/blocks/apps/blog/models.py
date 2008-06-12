from django.db import models
from django.core import validators
from blocks.apps.contenttypes.base import STATUS_CHOICES, WEIGHT_CHOICES, _
from blocks.apps.wiki import wiki

class BlogEntry(models.Model):
    # content
    title = models.CharField(_('title'), max_length=200, unique=True)
    lead_wiki = models.TextField(_('lead'))
    body_wiki = models.TextField(_('body'))
    
    # publishing options
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, default='N')
    publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"), blank=True)
    promoted = models.BooleanField(_('promoted'), help_text=_("promoted to frontpage or section"))
    
    comments_enabled = models.BooleanField(_('comments enabled'), help_text=_("enable comments for this entry"))
    
    def _get_lead(self):
        return wiki.parse(self.lead_wiki)
    lead = property(_get_lead)
    
    def _get_body(self):
        return wiki.parse(self.body_wiki)
    body = property(_get_body)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        db_table = 'blocks_blog_entry'
        verbose_name_plural = _('Blog Entries')
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

    class Admin:
        fields = (
           (None, {'fields': ('title', 'lead_wiki', 'body_wiki')}),
           (_('Publishing options'), {'fields': ('status', 'publish_date', 'promoted', 'comments_enabled'), 'classes': 'collapse'}),
        )
        list_filter = ('title',)
        list_display = ('publish_date', 'title')

