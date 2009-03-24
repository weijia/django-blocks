from django.template import Variable
from django.utils.html import strip_tags

class Field(object):
    def __init__(self, name):
        self.name = name
        self.value = None
        self.tag = name.split('.')[-1].lower()
    
    def resolve(self, model_instance):
        self.value = Variable(self.name).resolve(model_instance)
        return self.value

class TextField(Field):
    pass

class StripTagsField(Field):
    def resolve(self, model_instance):
        super(StripTagsField, self).resolve(model_instance)
        self.value = strip_tags(self.value)
        return self.value