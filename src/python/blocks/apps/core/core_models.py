from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

from blocks.apps.core.managers import STATUS_CHOICES, BaseManager
from blocks import forms

import re
LINKS_PA1 = re.compile('<a [^>]*href="[^"]*"[^>]*>[^<]*</a>')
LINKS_PA2 = re.compile('<a ([^>]*href="[^"]*"[^>]*>[^<]*)</a>')
LINKS_PB1 = re.compile('<a [^>]*target="[^"]*"[^>]*>[^<]*</a>')
LINKS_PB2 = re.compile('<a ([^>]*)(target="[^"]*" )([^>]*>[^<]*)</a>')
LINKS_ABS = re.compile('<a [^>]*href="https?://')
LINKS_REL = re.compile('<a [^>]*href="[.]?/?')
	
class Image(models.Model):
	article = None

	image = forms.BlocksImageField(_('image'), upload_to='images', sizes=settings.BLOCKS_IMAGE_SIZES)
	description = models.CharField(_('description'), max_length=255)

	def __unicode__(self):
		return u'%s: %s' % (self.article, self.image.name)

	class Meta:
		abstract = True
		verbose_name = _('Image')
		verbose_name_plural = _('Images')

def mark_external_links(text):

	LINKS_DOM = re.compile('<a [^>]*href="https?://%s' % Site.objects.get_current().domain.replace('.', '\.'))

	diff = 0
	for m in LINKS_PA1.finditer(text):
		pos = m.span()
		s = pos[0] + diff
		e = pos[1] + diff
		anc = text[s:e]
		if not ((LINKS_REL.match(anc) and not LINKS_ABS.match(anc)) or LINKS_DOM.match(anc)):
			rep = ''
			if LINKS_PB1.match(anc):
				rep = LINKS_PB2.sub('<a class="external" \g<2>\g<1>\g<3></a>', anc)
			else:
				rep = LINKS_PA2.sub('<a class="external" target="_blank" \g<1></a>', anc)
			diff +=  len(rep) - len(anc)
			text = "%s%s%s" % (text[:s], rep, text[e:])
	return text

class TranslationWrapper(object):
	def __init__(self, model):
		self.model = model

	def __getattr__(self, name):
		return mark_safe( mark_external_links(getattr(self.model, name, '')) )

class BaseModel(models.Model):
	name = models.CharField(_('name'), max_length=200, blank=False)

	def __unicode__(self):
		return u'%s' % (self.name)
	
	def get_history(self):
		 return LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.pk)

	def get_creation(self):
		lst = self.get_history().order_by('action_time')
		return lst[0] if len(lst) > 0 else None

	def get_lastchange(self):
		lst = self.get_history()
		return lst.latest('action_time') if len(lst) > 0 else None

	def _get_creation_date(self):
		l = self.get_creation()
		return l.action_time if l is not None else None
	creation_date = property(_get_creation_date)

	def _get_creation_user(self):
		l = self.get_creation()
		return l.user if l is not None else None
	creation_user = property(_get_creation_user)

	def _get_lastchange_date(self):
		l = self.get_lastchange()
		return l.action_time if l is not None else None
	lastchange_date = property(_get_lastchange_date)

	def _get_lastchange_user(self):
		l = self.get_lastchange()
		return l.user if l is not None else None
	lastchange_user = property(_get_lastchange_user)
	
	def get_translation(self, lang = None):
		if not lang:
			from django.utils.translation import trans_real
			lang = trans_real.get_language()

		trans = self.translations.filter(language = lang)
		if not trans:
			trans = self.translations.filter(language = settings.LANGUAGE_CODE)
		if not trans:
			return None
		return TranslationWrapper(trans[0])
	translation = property(get_translation)
	
	def _get_language(self):
		cnt = self.get_translation()
		if cnt is not None:
			return cnt.language
		else:
			return None
	locale = property(_get_language)

	class Meta:
		abstract = True

class BaseContentModel(BaseModel):
	# publishing options
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
	publish_date = models.DateTimeField(_('publish date'), help_text=_("auto publish at date expecified or when the content was published"), null=True, blank=True)
	unpublish_date = models.DateTimeField(_('unpublish date'), help_text=_("auto unpublish at date expecified"), null=True, blank=True)
	promoted = models.BooleanField(_('promoted'))

	# model manager
	objects = BaseManager()

	def save(self, force_insert=False, force_update=False):
		from datetime import datetime
		if self.status == 'P' and self.publish_date == None:
			self.publish_date = datetime.now()
		if self.status == 'D' and self.unpublish_date == None:
			self.unpublish_date = datetime.now()
		super(BaseContentModel, self).save(force_insert, force_update)
	
	class Meta:
		db_table = 'blocks_content'
		ordering = ('-publish_date',)


class BaseContentTranslation(models.Model):
	"""
	Base content translation - language-based
	"""
	model = None
	language  = models.CharField(max_length=5, choices=settings.BLOCKS_LANGUAGES, editable=True)

	def __unicode__(self):
		return u'%s: %s' % (self.model, self.language)

	class Meta:
		abstract = True
		ordering = ["id"] # sets up default ordering by language


#from django.dispatch import dispatcher
#from django.db.models import signals
#
#def change_watcher(sender, instance, signal, *args, **kwargs):
#	print "SIGNAL:", sender, signal, args, kwargs
#
#signals.post_init.connect(change_watcher, sender=BaseModel, signal=signals.post_init)
