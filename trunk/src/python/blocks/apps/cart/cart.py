import datetime
import random
import hashlib

from django.conf import settings
from blocks.apps.cart import models

CART_ID = 'BLOCKS_CARTID'
CART_HASH = 'BLOCKS_CARTHASH'

class Cart:
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        cart_hash = request.session.get(CART_HASH)
        self.cart = self.get(request, cart_id, cart_hash)
        
    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def __unicode__(self):
        return u'%s' % self.cart
    items = property(__iter__)
    
    def get_items_count(self):
        return self.cart.item_set.count()
    items_count = property(get_items_count)
    
    def get_total_price(self):
        total_price = 0;
        for item in self.items:
            total_price = total_price + item.total_price
        return total_price
    total_price = property(get_total_price)
    
    def get(self, request, cart_id=None, cart_hash=None):
        cart = None
        if cart_id and cart_hash:
            try:
                cart = models.Cart.objects.get(pk=cart_id, hash=cart_hash)
            except models.Cart.DoesNotExist:
                pass
        
        if not cart:
            cart = self.new(request)
            
        return cart
    
    def new(self, request):
        hash = hashlib.sha256(str(random.random()) + settings.SECRET_KEY).hexdigest()
        cart = models.Cart(creation_date=datetime.datetime.now(), hash=hash)
        cart.save()
        request.session[CART_ID] = cart.id
        request.session[CART_HASH] = cart.hash
        return cart

    def add(self, object, unit_price, quantity=1, tax=1 ):
        quantity = convert_to_int(quantity or 1, 1)
        try:
            item = models.Item.objects.get(cart=self.cart, object=object)
            item.quantity = item.quantity + quantity
            item.save()
        except models.Item.DoesNotExist:
            item = models.Item(
                cart=self.cart,
                object=object,
                unit_price=unit_price,
                quantity=quantity,
                tax=tax
            )
            item.save()
            
    def update(self, object, unit_price, quantity=0, tax=1):
        quantity = convert_to_int(quantity or 0)
        try:
            item = models.Item.objects.get(cart=self.cart, object=object)
            if int(quantity) == 0:
                self.remove(object)
            else:
                item.quantity = quantity
                item.save()
        except models.Item.DoesNotExist:
            pass
        
    def checkout(self, request):
        self.cart.status = 'CK'
        self.cart.save()
        self.clear(request)

    def remove(self, object):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                object=object,
            ).delete()
        except models.Item.DoesNotExist:
            pass
           
    def delete(self):
        self.cart.delete()
        
    def clear(self, request):
        request.session.pop(CART_ID)
        request.session.pop(CART_HASH)
        self.cart = None

def convert_to_int(value, default=0):
    if isinstance(value, str) or isinstance(value, unicode):
        return int(float(value.replace(',', '.')))
    elif isinstance(value, float):
        return int(float)
    return default
    