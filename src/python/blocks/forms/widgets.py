from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from symbol import except_clause
import os

class DelAdminFileWidget(AdminFileWidget):
    '''
    A AdminFileWidget that shows a delete checkbox
    '''
    input_type = 'file'

    def render(self, name, value, attrs=None):
        input = super(forms.widgets.FileInput, self).render(name, value, attrs)
        if value:
            from blocks.forms import fields
            thumbnail = None
            #if isinstance(value, fields.BlocksImageField):
            try:
                thumbnail = getattr(value, 'thumbnail')
            except AttributeError:
                pass

            item = '<div><label>%s</label>%s</div>'
            output = []
            output.append('<div class="form-row">')
            if isinstance(value, fields.BlocksImageField) and thumbnail != None:
                output.append(item % (_('Currently:'), '<img src="%s%s" alt="%s"/>' % (settings.MEDIA_URL, thumbnail.name, value)))
            output.append(item % (_('Change:'), input))
            if isinstance(value, fields.BlocksImageField):
                output.append(item % (_('Delete') + ':', '<input type="checkbox" name="%s_delete"/>' % name)) # split colon to force "Delete" that is already translated
            output.append('</div>')
            return mark_safe(u''.join(output))
        else:
            return mark_safe(input)

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(DelAdminFileWidget, self).value_from_datadict(data, files, name)
        else:
            return '__deleted__'
