from django.conf.urls.defaults import *

from blocks.apps.cart.views import *

urlpatterns = patterns('',
    url(r'^cart/add/$', cart_add_item, name="cart_add"),
    url(r'^cart/remove/$', cart_removed_item, name="cart_remove"),
    url(r'^cart/$', cart_detail, name="cart_detail"),
)