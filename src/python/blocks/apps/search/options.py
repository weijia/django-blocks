from django.core.exceptions import FieldError
from blocks.apps.search.fields import Field, TextField, StripTagsField

class ModelSearch(object):
    title = None
    fields = None
    
    def __init__(self, model, site, manager=None):
        self.model = model
        self.site = site
        self.manager = manager or model._default_manager
        self._fields = self.fields
    
    def instanciate(self, model_instance):
        self.fields = self._parse_fields(model_instance)
        self.guid = self._parse_guid(model_instance)
        
    def get_identifier(self):
        self.guid
    
    def _parse_guid(self, model_instance):
        """
        Get an unique identifier for the object.

        If not overridden, uses <app_label>.<object_name>.<pk>.
        """
        return "model://%s/%s/%s" % (model_instance._meta.app_label, model_instance._meta.module_name, model_instance._get_pk_val())

    def _parse_field(self, field, model_instance):
        if isinstance(field, str):
            field = TextField(field)
        if not isinstance(field, Field):
            raise FieldError, "%s is not a valid field" % field
        field.resolve(model_instance)
        return field
            
    def _parse_fields(self, model_instance):
        all_fields = []
        all_fields.append(self._parse_field(self.title, model_instance))
        for f in self._fields:
            all_fields.append(self._parse_field(f, model_instance))
        return all_fields
    
