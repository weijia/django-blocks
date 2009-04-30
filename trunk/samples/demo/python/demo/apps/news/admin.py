from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from blocks.apps.core.admin import BaseContentAdmin, MultiImageTabular, MultiLanguageInline
from demo.apps.news import models


#
# help
#
settings.BLOCKS_ADMIN_HELP['news'] = {
    '__label__':    _('News'),
    '__help__':     _('Manage News contents'),

    'newsarticle':  _('Edit and create the News Articles of the site'),
    'newstype':     _('Manage the News Articles Types of the site'),

}


#
# NewsArticle
#
class NewsArticleInline(MultiLanguageInline):
    model = models.NewsArticleTranslation

class NewsArticleAdmin(BaseContentAdmin):
    inlines = [NewsArticleInline]
    fieldsets = (
       (None,                    {'fields': ('name', 'date', 'local', 'image', 'srcname', 'srcurl', 'tag_list',)}),
       BaseContentAdmin.PUBLISHING_OPTIONS,
    )

admin.site.register(models.NewsArticle, NewsArticleAdmin)