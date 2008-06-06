from django.db import models
from django.contrib import admin

class Feed(models.Model):
    title = models.CharField(max_length=500)
    feed_url = models.URLField(unique=True, max_length=500)
    public_url = models.URLField(max_length=500)
    is_defunct = models.BooleanField()

    class Meta:
        db_table = 'aggregator_feeds'

    def __unicode__(self):
        return self.title

class FeedAdmin(admin.ModelAdmin):
    search_fields = ('title',)

admin.site.register(Feed, FeedAdmin)

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=500)
    summary = models.TextField(blank=True)
    date_modified = models.DateTimeField()
    guid = models.CharField(max_length=500, unique=True, db_index=True)

    class Meta:
        db_table = 'aggregator_feeditems'
        ordering = ("-date_modified",)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link
