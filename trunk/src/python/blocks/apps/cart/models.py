from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class ItemManager(models.Manager):
	def get(self, *args, **kwargs):
		if 'object' in kwargs:
			object = kwargs['object']
			kwargs['content_type'] = ContentType.objects.get_for_model(type(object))
			kwargs['object_id'] = object.pk
			del(kwargs['object'])
		return super(ItemManager, self).get(*args, **kwargs)

STATUS_CHOICES = (
	('',   _('None')),
	('CK', _('New')), 
	('RV', _('Reviewed')), 
	('AA', _('Aproved and Awaiting')), 
	('AS', _('Aproved and Sent')), 
	('RJ', _('Rejected')), 
)

class Cart(models.Model):
	hash = models.CharField(max_length=64)
	creation_date = models.DateTimeField(verbose_name=_('creation date'))
	
	user =  models.ForeignKey(User, null=True, blank=True)
	status = models.CharField(_('status'), max_length=2, choices=STATUS_CHOICES)

	class Meta:
		db_table = 'blocks_cart'
		verbose_name = _('cart')
		verbose_name_plural = _('carts')
		ordering = ('-creation_date',)

	def __unicode__(self):
		return u'%s - %s (%s)' % (self.id, self.user, self.status)


class Item(models.Model):
	cart = models.ForeignKey(Cart, verbose_name=_('cart'))
	quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
	unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
	tax = models.DecimalField(max_digits=5, decimal_places=3, verbose_name=_('tax'))
	
	# product as generic relation
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()

	objects = ItemManager()

	class Meta:
		db_table = 'blocks_cart_item'
		verbose_name = _('item')
		verbose_name_plural = _('items')
		ordering = ('cart',)

	def __unicode__(self):
		return self.object

	def total_price(self):
		return self.quantity * self.unit_price
	total_price = property(total_price)

	# product
	def get_object(self):
		return self.content_type.get_object_for_this_type(id=self.object_id)

	def set_object(self, object):
		self.content_type = ContentType.objects.get_for_model(type(object))
		self.object_id = object.pk

	object = property(get_object, set_object)

