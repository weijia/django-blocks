from django.db import models
from django.core import validators
from blocks.apps.contenttypes.base import STATUS_CHOICES, WEIGHT_CHOICES, _
from blocks.apps.wiki import wiki
from blocks.core import middleware as ThreadLocals
import datetime

class BlogEntry(models.Model):
    # content
    title = models.CharField(_('title'), max_length=200, unique=True)
    lead_wiki = models.TextField(_('lead'))
    body_wiki = models.TextField(_('body'))
    
    # publishing options
    publish_date = models.DateTimeField(_('publish date'), blank=True)
    modified_date = models.DateTimeField(_('modified date'), blank=True)
    #author = models.CharField(_('author'), max_length=50, blank=True, editable=False)
    author = models.CharField(_('author'), max_length=80, blank=True)
    
    comments_enabled = models.BooleanField(_('comments enabled'), help_text=_("enable comments for this entry"))
    
    
    def _get_lead(self):
        return wiki.parse(self.lead_wiki)
    lead = property(_get_lead)
    
    def _get_body(self):
        return wiki.parse(self.body_wiki)
    body = property(_get_body)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        year = self.publish_date.strftime("%Y").lower()
        month = self.publish_date.strftime("%b").lower()
        day = self.publish_date.strftime("%d").lower()
        
        from blocks.core import utils
        return utils.get_url('blog-details', [year, month, day, self.id])
    
    def save(self):
        if not self.author:
            user = ThreadLocals.get_current_user()
            author = ''
            try:
                if user.first_name or user.last_name:
                    author = (user.first_name + ' ' + user.last_name).strip()
                elif user.username:
                    author = user.username.strip()
            except AttributeError:
                pass
            
            if author:
                self.author = author
            else:
                self.author = 'anonymous'
        if not self.publish_date:
            self.publish_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        super(BlogEntry, self).save()
    
    class Meta:
        db_table = 'blocks_blog_entry'
        verbose_name_plural = _('Blog Entries')
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

    class Admin:
        fields = (
           (None, {'fields': ('title', 'lead_wiki', 'body_wiki')}),
           (_('Publishing options'), {'fields': ('publish_date', 'modified_date', 'author', 'comments_enabled'), 'classes': 'collapse'}),
        )
        list_filter = ('title',)
        list_display = ('title', 'author', 'publish_date')

