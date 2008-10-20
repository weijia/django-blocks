from django.db import models
from django.contrib import admin

from blocks.apps.core.base import STATUS_CHOICES, WEIGHT_CHOICES, _

class BaseModel(models.Model):
    name = models.CharField(_('name'), max_length=80, unique=True)
    description = models.CharField(_('description'), max_length=255)
    
    class Meta:
        abstract = True
        ordering = ('name',)

class BaseContentModel(models.Model):
    # content title
    title = models.CharField(_('title'), max_length=200, unique=True)
    
    # publishing options
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"), null=True, blank=True)
    unpublish_date = models.DateTimeField(_('unpublish date'), help_text=_("auto unpublish at date expecified"), null=True, blank=True)
    headline = models.BooleanField(_('headline'), help_text=_("headline the content"))
        
    class Meta:
        db_table = 'blocks_content'
        ordering = ('publish_date',)

class BaseContentAdmin(admin.ModelAdmin):    
    fieldsets = (
       (None,                    {'fields': ('title',)}),
       (_('Publishing Options'), {'fields': ('publish_date', 'unpublish_date', 'status',), 'classes': ('collapse', )}),
    )
    list_filter = ('status',)
    search_fields = ('title',)
    list_display = ('title', 'status')