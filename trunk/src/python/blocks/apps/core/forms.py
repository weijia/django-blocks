from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from blocks.apps.core.models import StaticPage

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class StaticPageAdminForm(forms.ModelForm):
    class Meta:
        model = StaticPage

    def clean_menu(self):
        menu = self.cleaned_data['menu']
        name = self.cleaned_data['name']

        relative = None
        try:
            relative = self.data['relative']
        except:
            pass
               
        slug = slugify(name)
        url = menu if not relative else "%s%s/" % (menu, slug)
    
        f = None
        
        # check if there's match first
        try:
            f = StaticPage.objects.get(url__exact=url)
        except StaticPage.DoesNotExist:
            pass
        
        if f:
            raise forms.ValidationError(_("can't associate more than one page to the same menu (url)"))

        # Always return the cleaned data, whether you have changed it or not.
        return menu

