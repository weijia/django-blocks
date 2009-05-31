from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from blocks.apps.cart import Cart

def _get_object(queryset, object_id):
    queryset = queryset._clone()
    queryset = queryset.filter(pk=object_id)
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404, "No %s found matching the query" % (queryset.model._meta.verbose_name)
    return obj

def cart_add_item(request, queryset, object_id, quantity):
    obj = _get_object(queryset, object_id)
    price = obj.unit_price
    cart = Cart(request)
    cart.add(obj, price, quantity)
    return HttpResponseRedirect(reverse('cart_detail'))
    
def cart_remove_item(request, queryset, object_id):
    obj = _get_object(queryset, object_id)
    cart = Cart(request)
    cart.remove(obj)
    return HttpResponseRedirect(reverse('cart_detail'))

def cart_checkout(request):
    pass

def cart_detail(request):
    return direct_to_template(request, template='blocks/cart_detail.html', extra_content={'cart': Cart(request)} )