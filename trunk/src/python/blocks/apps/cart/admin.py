from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

from blocks.apps.cart.models import Cart
from blocks.apps.shop.models import Tax


class CartAdminForm(ModelForm):
	class Meta:
		model = Cart
		fields = ['status',]

class CartAdmin(admin.ModelAdmin):
	form = CartAdminForm
	list_filter = ('status', )
	search_fields = ('status',)
	list_display = ('user', 'creation_date', 'status', )
	
	def get_urls(self):
		from django.conf.urls.defaults import patterns, url
		from django.utils.functional import update_wrapper
		
		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)
		
		urls = super(CartAdmin, self).get_urls()
		urlpatterns = patterns('',
			(r'^(?P<cart_pk>[-\w]+)/$', wrap(self.update_cart_item)),
		)
		return urlpatterns + urls

	def update_cart_item(self, request, cart_pk):
		from blocks.apps.cart import Cart as ShoppingCart
		cart = ShoppingCart()
		cart.cart = Cart.objects.get(pk=cart_pk)
		return super(CartAdmin, self).change_view(request, cart_pk, extra_context={'cart': cart,})
	
admin.site.register(Cart, CartAdmin)

class TaxAdmin(admin.ModelAdmin):
	"""
	"""
	pass

admin.site.register(Tax, TaxAdmin)