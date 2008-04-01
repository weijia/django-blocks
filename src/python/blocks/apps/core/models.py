from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from base import STATUS_CHOICES

class Template(models.Model):
	name = models.CharField(_('name'), max_length=80, unique=True)
	description = models.CharField(_('description'), max_length=255)
	
	class Meta:
		db_table = 'blocks_template'
	
	class Admin:
		pass

class View(models.Model):
	name = models.CharField(_('name'), max_length=80, unique=True)
	title = models.CharField(_('title'), max_length=200)
	description = models.CharField(_('description'), max_length=255)
	
	url = models.CharField(_('URL'), max_length=100, validator_list=[validators.isAlphaNumericURL], db_index=True,
		help_text=_("Example: '/about/contact/'. Make sure to have leading and trailing slashes."))
	
	template = models.OneToOneField(Template, verbose_name=_('template'),
		help_text=_("You must provide a template to be used in this page"))
	
	registration_required = models.BooleanField(_('registration required'),
		help_text=_("If this is checked, only logged-in users will be able to view the page."))
	
	class Meta:
		db_table = 'blocks_view'
		verbose_name = _('page')
		verbose_name_plural = _('pages')
		ordering = ('name',)
		
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