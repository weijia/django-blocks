# -*- coding: utf-8 -*-
# $Id$
#
# Shop app django models
#from decimal import Decimal

from django.conf import settings

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from blocks.forms import BlocksImageField

class TaxManager(models.Manager):
	"""
	"""
	pass

class Tax(models.Model):
	"""
	A product tax
	"""
	tax = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_('tax'))

	objects = TaxManager()

	def __unicode__(self):
		nmr = self.tax * 100
		return '%s%' % nmr

class AssetManager(models.Manager):
	"""
	"""
	pass

class Asset(models.Model):
	"""
	A sellable asset
	"""
	tax = models.ForeignKey(Tax, null=False, blank=False)

	# related model as generic relation
	content_type	= models.ForeignKey(ContentType)
	object_id		= models.PositiveIntegerField()
	content_object	= generic.GenericForeignKey('content_type', 'object_id')

	objects = AssetManager()
	
	class Meta:
		db_table			= 'blocks_shop_asset'
		verbose_name		= _('asset')
		verbose_name_plural = _('assets')

class AssetKindManager(models.Manager):
	"""
	"""
	pass

class AssetKind(models.Model):
	"""
	A sellable asset kind
	"""

	asset = models.ForeignKey(Asset, null=False, blank=False)

	reference	= models.CharField(_('reference'), max_length=50, null=True, blank=True)
	unit_price	= models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
	image		= BlocksImageField(_('image'), upload_to='images/shop/assets',
		sizes=[('thumbnail', 160, 145), ('detail', 275, 335), ])

	objects = AssetKindManager()
	
	class Meta:
		db_table			= 'blocks_shop_asset_kind'
		verbose_name		= _('asset kind')
		verbose_name_plural = _('asset kinds')
