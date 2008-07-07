from django.db import models
from django.contrib import admin

class Feed(models.Model):
    title = models.CharField(max_length=300)
    feed_url = models.URLField(unique=True, max_length=300)
    public_url = models.URLField(max_length=300)

    class Meta:
        db_table = 'aggregator_feeds'

    def __unicode__(self):
        return self.title

#class FeedAdmin(admin.ModelAdmin):
    class Admin:
        search_fields = ('title',)
        list_display = ('title', 'public_url',)

#admin.site.register(Feed, FeedAdmin)

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=300)
    link = models.URLField(max_length=300)
    summary = models.TextField(blank=True)
    date_modified = models.DateTimeField()
    guid = models.CharField(max_length=300, unique=True, db_index=True)
    
    def _get_description(self):
        from django.utils.text import truncate_words
        from blocks.core.utils import strip_tags
        return strip_tags(truncate_words(self.summary, 100), ('blockquote', 'code', 'img', 'script', 'style', 'iframe', 'object'))
    description = property(_get_description)

    class Meta:
        db_table = 'aggregator_feeditems'
        ordering = ("-date_modified",)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link
