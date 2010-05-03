# -*- coding: utf-8 -*-
# $Id$
#
# Demo catalog models

from django.db import models
from django.utils.translation import ugettext_lazy as _

from blocks.apps.core import core_models

class CategoryManager(models.Manager):
	"""
	"""
	def children(self):
		_children = Category.objects.filter(parent=self).order_by('name',)
		for child in _children:
			child.parent = self # Hack to avoid unnecessary DB queries further down the track.
		return _children

	def has_children(self):
		return self.children().count() > 0

class Category(core_models.BaseModel):
	"""
	A product category
	"""
	parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)

	objects = CategoryManager()

	class Meta:
		db_table			= 'shop_category'
		verbose_name		= _('category')
		verbose_name_plural = _('categories')
		ordering			= ('name',)

class CategoryTranslation(models.Model):
	"""
	"""
	article		= models.ForeignKey(Category, related_name="translations")
	language	= models.CharField(max_length=25, choices=settings.BLOCKS_LANGUAGES, editable=True)

	title = models.CharField(_('title'), max_length=200)
	description = models.TextField(_('description'), max_length=64000, blank=True)

	def __unicode__(self):
		return u'%s: %s' % (self.article, self.language)

	class Meta:
		db_table			= 'shop_category_translation'
		ordering			= ["id"] # sets up default ordering by language
		verbose_name		= _('Category Translation')
		verbose_name_plural = _('Category Translations')

class ProductManager(models.Manager):
	"""
	"""
	pass

class Product(core_models.BaseModel):
	"""
	A product
	"""

	category = models.ForeignKey(Category, null=False, blank=False)
	
	objects = ProductManager()

	class Meta:
		db_table			= 'shop_product'
		verbose_name		= _('product')
		verbose_name_plural = _('products')

class ProductTranslation(models.Model):
	article		= models.ForeignKey(Product, related_name="translations")
	language	= models.CharField(max_length=25, choices=settings.BLOCKS_LANGUAGES, editable=True)

	title = models.CharField(_('title'), max_length=200)
	description = models.TextField(_('description'), max_length=64000, blank=True)

	def __unicode__(self):
		return u'%s: %s' % (self.article, self.language)

	class Meta:
		db_table			= 'shop_product_translation'
		ordering			= ["id"] # sets up default ordering by language
		verbose_name		= _('Product Translation')
		verbose_name_plural = _('Product Translations')
