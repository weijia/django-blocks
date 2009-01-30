from django.forms.fields import ImageField, CharField

class BlocksImageFormField(ImageField):
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(BlocksImageFormField, self).clean(data, initial)
        else:
            return '__deleted__'

class GeoLocationFormField(CharField):
    pass
