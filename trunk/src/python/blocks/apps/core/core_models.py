from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from blocks.apps.core.managers import STATUS_CHOICES, BaseManager

#class BaseModel(models.Model):
#    name = models.CharField(_('name'), max_length=80, unique=True)
#    description = models.CharField(_('description'), max_length=255)
#
#    class Meta:
#        abstract = True
#        ordering = ('name',)

class BaseModel(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True, blank=False)

    def __unicode__(self):
        return u'%s' % (self.name)
    
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
    # publishing options
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"), null=True, blank=True)
    unpublish_date = models.DateTimeField(_('unpublish date'), help_text=_("auto unpublish at date expecified"), null=True, blank=True)
    promoted = models.BooleanField(_('promoted'))

    # model manager
    objects = BaseManager()
    
    class Meta:
        db_table = 'blocks_content'
        ordering = ('-publish_date',)


class BaseContentTranslation(models.Model):
    """
    Base content translation - language-based
    """
    model = None
    language  = models.CharField(max_length=2, choices=settings.BLOCKS_LANGUAGES, editable=True)

    def __unicode__(self):
        return u'%s: %s' % (self.model, self.language)

    class Meta:
        abstract = True
        ordering = ["id"] # sets up default ordering by language



class BaseAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("blocks/css/jquery-tabs.css", "blocks/css/jquery.wysiwyg.css",) }
        js = (
            "blocks/js/jquery.js",
            "blocks/js/jquery-ui.js",
            "blocks/js/jquery.wysiwyg.js",
            "blocks/js/lang.js",
        )


class BaseContentAdmin(BaseAdmin):
    PUBLISHING_OPTIONS = (_('Publishing Options'), {'fields': ('publish_date', 'unpublish_date', 'promoted', 'status',), 'classes': ('collapse', )})
    fieldsets = (
       (None,                    {'fields': ('name',)}),
       PUBLISHING_OPTIONS,
    )
    list_filter = ('status', 'promoted')
    search_fields = ('name',)
    list_display = ('name', 'creation_user', 'lastchange_date', 'status', 'promoted')



class MultiLanguageInline(admin.options.InlineModelAdmin):
    template = 'blocks/multilang.html'
    extra = len(settings.LANGUAGES) if settings.USE_I18N else 1
    max_num = len(settings.LANGUAGES) if settings.USE_I18N else 1

class MultiImageTabular(admin.options.InlineModelAdmin):
    template = 'blocks/imagetabular.html'

#from django.dispatch import dispatcher
#from django.db.models import signals
#
#def change_watcher(sender, instance, signal, *args, **kwargs):
#    print "SIGNAL:", sender, signal, args, kwargs
#
#signals.post_init.connect(change_watcher, sender=BaseModel, signal=signals.post_init)
