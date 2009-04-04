from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class BaseContentAdminForm(forms.ModelForm):
    class Meta:
        pass
        #model = BaseContentModel
        
    def clean_name(self):
        from blocks.apps.core.core_models import BaseContentModel
        name = self.cleaned_data['name']
        f = None        
        try:
            if self.instance.pk is not None:
                f = BaseContentModel.objects.filter(name__exact=name).exclude(pk=self.instance.pk)
            else:
                f = BaseContentModel.objects.filter(name__exact=name)
        except BaseContentModel.DoesNotExist:
            pass
        
        if f:
            raise forms.ValidationError(_("can't have more than one content with the same name"))

        # Always return the cleaned data, whether you have changed it or not.
        return name
    

class StaticPageAdminForm(forms.ModelForm):
    class Meta:
        from blocks.apps.core.models import StaticPage
        model = StaticPage

    def clean_menu(self):
        from blocks.apps.core.models import StaticPage
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
        try:
            if self.instance.pk is not None:
                f = StaticPage.objects.filter(url__exact=url).exclude(pk=self.instance.pk)
            else:
                f = StaticPage.objects.filter(url__exact=url)
        except StaticPage.DoesNotExist:
            pass
        
        if f:
            raise forms.ValidationError(_("can't associate more than one page to the same menu (url: %s)") % url)

        # Always return the cleaned data, whether you have changed it or not.
        return menu

