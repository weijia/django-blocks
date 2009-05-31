import datetime
import random
import hashlib

from django.conf import settings
from blocks.apps.cart.models import Cart, Item

CART_ID = 'BLOCKS_CARTID'

class Cart:
    def __init__(self, request):
        self.request = request
        cart_id = request.session.get(CART_ID)
        self.cart = self.get(cart_id)
        
    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def get(self, card_id=None):
        if cart_id:
            try:
                cart = Cart.objects.get(hash=cart_id)
            except Cart.DoesNotExist:
                cart = self.new()
        else:
            cart = self.new()
        return cart
    
    def new(self):
        hash = hashlib.sha256(str(random.random()) + settings.SECRET_KEY).hexdigest()
        cart = Cart(creation_date=datetime.datetime.now(), hash=hash)
        cart.save()
        self.request.session[CART_ID] = cart.hash
        return cart

    def add(self, object, unit_price, quantity=1, tax=1 ):
        try:
            item = Item.objects.get(cart=self.cart, object=object)
        except Item.DoesNotExist:
            item = Item(
                cart=self.cart,
                object=object,
                unit_price=unit_price,
                quantity=quantity,
                tax=tax
            )
            item.save()
        else:
            pass
            # just update the object

    def remove(self, object):
        try:
            item = Item.objects.get(
                cart=self.cart,
                object=object,
            ).delete()
        except Item.DoesNotExist:
            pass
           

    def clear(self):
        self.cart.delete()
        self.request.session.pop(CART_ID)

