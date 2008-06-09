from django.db import models
from django.contrib import admin
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from base import *
from blocks.apps.wiki import wiki

class BaseModel(models.Model):
    name = models.CharField(_('name'), max_length=80, unique=True)
    description = models.CharField(_('description'), max_length=255)
    
    class Meta:
        abstract = True
        ordering = ('name',)

class BaseContentModel(models.Model):
    # content
    title = models.CharField(_('title'), max_length=200, unique=True)
    lead_wiki = models.TextField(_('lead'))
    body_wiki = models.TextField(_('body'))
    
    # publishing options
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, default='N')
    publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"), null=True, blank=True)
    unpublish_date = models.DateTimeField(_('unpublish date'), help_text=_("auto unpublish at date expecified"), null=True, blank=True)
    promoted = models.BooleanField(_('promoted'), help_text=_("promoted to frontpage or section"))
    weight = models.IntegerField(choices=WEIGHT_CHOICES, null=True, blank=True)
    
    def _get_lead(self):
        return wiki.parse(self.lead_wiki)
    lead = property(_get_lead)
    
    def _get_body(self):
        return wiki.parse(self.body_wiki)
    body = property(_get_body)
    
    class Meta:
        db_table = 'blocks_content'
        ordering = ('weight', 'publish_date',)

class Template(BaseModel):
    template = models.CharField(_('template'), max_length=70,
                    help_text=_("Example: 'homepage.html'. If this isn't provided, the system will use 'default.html'."))

    def delete(self):
        # TODO: validate if is system Template
        if self.name == "Default":
          return
        else:
          super(Template, self).delete()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = 'blocks_template'


#class TemplateAdmin(admin.ModelAdmin):
    class Admin:
        search_fields = ('template', 'name', 'description')

#admin.site.register(Template, TemplateAdmin)


#class Page(BaseModel):
#    title = models.CharField(_('title'), max_length=200)
#    
#    url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True,
#        help_text=_("URL by which this page would be accessed. For example, type '/about/' when writing an about page. Use a relative path make sure to have leading and trailing slashes."))
#    
#    template = models.OneToOneField(Template, verbose_name=_('template'),
#        help_text=_("You must provide a template to be used in this page"))
#    
#    registration_required = models.BooleanField(_('registration required'),
#        help_text=_("If this is checked, only logged-in users will be able to view the page."))
#    
#    class Meta:
#        db_table = 'blocks_page'
#        
#    def __unicode__(self):
#        return u"%s -- %s" % (self.url, self.title)
#
#    def get_absolute_url(self):
#        return self.url
#
#class PageAdmin(admin.ModelAdmin):
#    fields = (
#        (None, {'fields': ('name', 'url')}),
#        (_('Advanced options'), {'classes': 'collapse', 'fields': ('registration_required', 'template')}),
#    )
#    list_filter = ('template',)
#    search_fields = ('url', 'title')
#
#admin.site.register(Page, PageAdmin)


#class View(BaseModel):
#    class Meta:
#        db_table = 'blocks_view'
#        app_label = 'blocks'
#
#admin.site.register(View)


#class StaticPage(BaseContentModel):
class StaticPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL],  unique=True, 
        help_text=_("Example: '/about/'. Make sure to have leading and trailing slashes."))
    # content
    title = models.CharField(_('title'), max_length=200)
    lead_wiki = models.TextField(_('lead'))
    body_wiki = models.TextField(_('body'))
    
    template = models.ForeignKey(Template, verbose_name=_('template'),
        help_text=_("You must provide a template to be used in this page."))
    
    menu = models.BooleanField(_('Menu'),
        help_text=_("Appears in the main menu."))
    
    def _get_lead(self):
        return wiki.parse(self.lead_wiki)
    lead = property(_get_lead)
    
    def _get_body(self):
        return wiki.parse(self.body_wiki)
    body = property(_get_body)
    
    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
        
#    def save(self):
#        if not self.status or self.status == "": self.status = 'P'
#        super(StaticPage, self).save()
        
    class Meta:
        db_table = 'blocks_static_page'
        verbose_name = _('static Page')
        verbose_name_plural = _('static Pages')

#class StaticPageAdmin(admin.ModelAdmin):    
    class Admin:
        fields = (
           (None, {'fields': ('url', 'title', 'lead_wiki', 'body_wiki')}),
           (_('Advanced options'), {'fields': ('template', 'menu',), 'classes': 'collapse'}),
            #(_('Publishing options'), {'classes': 'collapse', 'fields': ('status', 'publish_date', 'unpublish_date', 'weight', 'promoted')}),
        )
        list_filter = ('template',)
        search_fields = ('template', 'title',)

#admin.site.register(StaticPage, StaticPageAdmin)
