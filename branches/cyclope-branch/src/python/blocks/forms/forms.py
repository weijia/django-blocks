from django.forms.fields import ImageField, CharField

class BlocksImageFormField(ImageField):
    def clean(self, data, initial=None):        
        if data and data['deleted'] != '__deleted__':
            data['file'] = super(BlocksImageFormField, self).clean(data['file'], initial)
        return data

class GeoLocationFormField(CharField):
    pass
