from django.db import models
from django.contrib import admin
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from blocks.apps.core import models as blocks

class StaticPage(blocks.BaseContentModel):
    url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True, unique=True, 
        help_text=_("Example: '/about/'. Make sure to have leading and trailing slashes."))

    template = models.ForeignKey(blocks.Template, verbose_name=_('template'),
        help_text=_("You must provide a template to be used in this page"))
    
    class Meta:
        db_table = 'blocks_content_page'
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')
        app_label = 'blocks'
        
    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
    
    def save(self):
        if not self.status or self.status == "": self.status = 'P'
        super(StaticPage, self).save()

class StaticPageAdmin(admin.ModelAdmin):
    fields = (
        (None, {'fields': ('url', 'title', 'lead_wiki', 'body_wiki')}),
        (_('Advanced options'), {'classes': 'collapse', 'fields': ('template',)}),
        #(_('Publishing options'), {'classes': 'collapse', 'fields': ('status', 'publish_date', 'unpublish_date', 'weight', 'promoted')}),
    )
    list_filter = ('template',)
    search_fields = ('template', 'title',)
        
admin.site.register(StaticPage, StaticPageAdmin)