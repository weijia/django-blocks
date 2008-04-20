#
# we are using the queryset-refactor branch
# see: http://code.djangoproject.com/wiki/QuerysetRefactorBranch
#
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from base import STATUS_CHOICES
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
	title = models.CharField(_('title'), max_length=80, unique=True)
	lead = models.TextField(_('lead'))
	body = models.TextField(_('body'))
	
	class Meta:
		db_table = 'blocks_content'
		ordering = ('title',)

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
		help_text=_("Example: '/about/'. Make sure to have leading and trailing slashes."))
	
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
		

class StaticPage(BaseContentModel):
	url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True,
		help_text=_("Example: '/about/'. Make sure to have leading and trailing slashes."))
	
	class Meta:
		db_table = 'blocks_content_page'

	class Admin:
		pass