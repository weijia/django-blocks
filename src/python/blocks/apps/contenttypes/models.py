from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from blocks.apps.core import models as blocks

class StaticPage(blocks.BaseContentModel):
    url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True,
        help_text=_("Example: '/about/'. Make sure to have leading and trailing slashes."))
    
    class Meta:
        db_table = 'blocks_content_page'
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')
        
    class Admin:
        fields = (
            (None, {'fields': ('title', 'lead', 'body')}),
            (_('Publishing options'), {'classes': 'collapse', 'fields': ('status', 'publish_date', 'unpublish_date', 'weight', 'promoted')}),
        )