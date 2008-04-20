#
# we are using the queryset-refactor branch
# see: http://code.djangoproject.com/wiki/QuerysetRefactorBranch
#
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from base import *
import logging

log = logging.getLogger("core.models")
log.debug("loading core models")

class BaseModel(models.Model):
	name = models.CharField(_('name'), max_length=80, unique=True)
	description = models.CharField(_('description'), max_length=255)
	
	class Meta:
		abstract = True
		ordering = ('name',)

class BaseContentModel(models.Model):
	# content
	title = models.CharField(_('title'), max_length=200, unique=True)
	lead = models.TextField(_('lead'))
	body = models.TextField(_('body'))
	
	# publishing options
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)
	publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"))
	unpublish_date = models.DateTimeField(_('unpublish date'), help_text=_("auto unpublish at date expecified"))
	promoted = models.BooleanField(_('promoted'), help_text=_("promoted to frontpage or section"))
	weight = models.IntegerField(choices=WEIGHT_CHOICES)
	
	class Meta:
		db_table = 'blocks_content'
		ordering = ('weight', 'publish_date',)

## Template Model
# syncdb will execute the sql/template.sql that populates table with default data
#
class Template(BaseModel):
	
	def delete(self):
		# TODO: validate if is system Template
		if self.name == "Default":
		  return
		else:
		  super(Template, self).delete()
			
	class Meta:
		db_table = 'blocks_template'
	
	class Admin:
		pass

class Page(BaseModel):
	title = models.CharField(_('title'), max_length=200)
	
	url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True,
		help_text=_("URL by which this page would be accessed. For example, type '/about/' when writing an about page. Use a relative path make sure to have leading and trailing slashes."))
	
	template = models.OneToOneField(Template, verbose_name=_('template'),
		help_text=_("You must provide a template to be used in this page"))
	
	registration_required = models.BooleanField(_('registration required'),
		help_text=_("If this is checked, only logged-in users will be able to view the page."))
	
	class Meta:
		db_table = 'blocks_page'
		
	class Admin:
		fields = (
			(None, {'fields': ('name', 'url')}),
			(_('Advanced options'), {'classes': 'collapse', 'fields': ('registration_required', 'template')}),
		)
		list_filter = ('template',)
		search_fields = ('url', 'title')

	def __unicode__(self):
		return u"%s -- %s" % (self.url, self.title)

	def get_absolute_url(self):
		return self.url

class View(BaseModel):
	class Meta:
		db_table = 'blocks_view'
	
	class Admin:
		pass
