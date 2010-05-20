from django.core.exceptions import FieldError
from blocks.apps.search.fields import Field, TextField, DateField, StripTagsField

class ModelSearch(object):
	title = None
	fields = None
	date = 'lastchange_date'
	keys = []
	
	def __init__(self, model, site, manager=None):
		self.model = model
		self.site = site
		self.manager = manager or model._default_manager
		self._fields = self.fields
		self._date_field = DateField(self.date)
		self.keys.append(Field('locale', 'lang'))
	
	def instanciate(self, model_instance, lang=None):
		self.fields = self._parse_fields(model_instance)
		self.guid = self._parse_guid(model_instance)
		self.date = self._parse_field(self._date_field, model_instance)
		if lang is not None:
			self.keys[0].value = lang
		return True
		
	def get_identifier(self):
		self.guid
	
	def _parse_guid(self, model_instance):
		"""
		Get an unique identifier for the object.

		If not overridden, uses <app_label>.<object_name>.<pk>.
		"""
		if model_instance is None:
			return "model://None"
		else:
			keys = '?'
			for f in self.fields:
				if f.key is not None:
					key = "%s=%s&" % (f.key, f.value)
					keys = keys + key
			keys = keys[:-1]
			return "model://%s/%s/%s%s" % (model_instance._meta.app_label, model_instance._meta.module_name, model_instance._get_pk_val(), keys)

	def _parse_field(self, field, model_instance):
		if isinstance(field, str):
			field = TextField(field)
		if not isinstance(field, Field):
			raise FieldError, "%s is not a valid field" % field
		if model_instance is not None:
			field.resolve(model_instance)
		return field
			
	def _parse_fields(self, model_instance):
		all_fields = []
		all_fields.append(self._parse_field(self.title, model_instance))
		for f in self.keys:
			all_fields.append(self._parse_field(f, model_instance))
		for f in self._fields:
			all_fields.append(self._parse_field(f, model_instance))
		return all_fields
	
