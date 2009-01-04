from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

from blocks.apps.core.base import STATUS_CHOICES, _

#class BaseModel(models.Model):
#    name = models.CharField(_('name'), max_length=80, unique=True)
#    description = models.CharField(_('description'), max_length=255)
#
#    class Meta:
#        abstract = True
#        ordering = ('name',)

class BaseModel(models.Model):

    def get_history(self):
         return LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.pk)

    def get_creation(self):
        return self.get_history().order_by('action_time')[0]

    def get_lastchange(self):
        return self.get_history().latest('action_time')

    def _get_creation_date(self):
        return self.get_creation().action_time
    creation_date = property(_get_creation_date)

    def _get_creation_user(self):
        return self.get_creation().user.username
    creation_user = property(_get_creation_user)

    def _get_lastchange_date(self):
        return self.get_lastchange().action_time
    lastchange_date = property(_get_lastchange_date)

    def _get_lastchange_user(self):
        return self.get_lastchange().user.username
    lastchange_user = property(_get_lastchange_user)

    def get_translation(self, lang = None):
        if not lang:
            from django.utils.translation import trans_real
            lang = trans_real.get_language()

        trans = self.translations.filter(language = lang)
        if not trans:
            trans = self.translations.filter(language = settings.LANGUAGE_CODE)
        if not trans:
            return None
        return trans[0]
    translation = property(get_translation)

    class Meta:
        abstract = True

class BaseContentModel(BaseModel):
    # content name
    name = models.CharField(_('name'), max_length=200, unique=True, blank=False)
    
    # publishing options
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"), null=True, blank=True)
    unpublish_date = models.DateTimeField(_('unpublish date'), help_text=_("auto unpublish at date expecified"), null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        db_table = 'blocks_content'
        ordering = ('publish_date',)


class BaseContentAdmin(admin.ModelAdmin):    
    fieldsets = (
       (None,                    {'fields': ('name',)}),
       (_('Publishing Options'), {'fields': ('publish_date', 'unpublish_date', 'status',), 'classes': ('collapse', )}),
    )
    list_filter = ('status',)
    search_fields = ('name',)
    list_display = ('name', 'creation_user', 'lastchange_date', 'status')

    class Media:
        css = {"all": ("blocks/css/jquery-tabs.css",) }
        js = ("blocks/js/jquery.js", "blocks/js/jquery-ui.js", "blocks/js/lang.js",)


class MultiLanguageInline(admin.options.InlineModelAdmin):
    template = 'blocks/multilang.html'

class MultiImageTabular(admin.options.InlineModelAdmin):
    template = 'blocks/imagetabular.html'

#from django.dispatch import dispatcher
#from django.db.models import signals
#
#def change_watcher(sender, instance, signal, *args, **kwargs):
#    print "SIGNAL:", sender, signal, args, kwargs
#
#signals.post_init.connect(change_watcher, sender=BaseModel, signal=signals.post_init)
