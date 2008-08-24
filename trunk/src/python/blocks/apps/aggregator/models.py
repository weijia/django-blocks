from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe

class Feed(models.Model):
    title = models.CharField(max_length=300)
    feed_url = models.URLField(unique=True, max_length=300)
    public_url = models.URLField(max_length=300)

    class Meta:
        db_table = 'aggregator_feeds'

    def __unicode__(self):
        return self.title

class FeedAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'public_url',)

admin.site.register(Feed, FeedAdmin)

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=300)
    link = models.URLField(max_length=300)
    summary_html = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    date_modified = models.DateTimeField()
    guid = models.CharField(max_length=300, unique=True, db_index=True)

    def _get_summary(self):
        return mark_safe(self.summary_html)
    summary = property(_get_summary)
    
    def _get_content(self):
        return mark_safe(self.content_html)
    content = property(_get_content)
    
    class Meta:
        db_table = 'aggregator_feeditems'
        ordering = ("-date_modified",)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link
