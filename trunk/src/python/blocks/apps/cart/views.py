from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from blocks.apps.cart import Cart

def _get_object(queryset, object_id):
    qs = queryset._clone()
    qs = qs.filter(pk=object_id)
    obj = None
    try:
        obj = qs.get()
    except qs.model.DoesNotExist:
        raise Http404, "No %s found matching the query" % (qs.model._meta.verbose_name)
    return obj

def cart_add_item(request, queryset, object_id):
    obj = _get_object(queryset, object_id)
    price = obj.unit_price
    cart = Cart(request)
    cart.add(obj, price, request.REQUEST.get('quantity'))
    return HttpResponseRedirect(reverse('blocks.cart_detail'))

def cart_update_item(request, queryset, object_id):
    obj = _get_object(queryset, object_id)
    price = obj.unit_price
    cart = Cart(request)
    cart.update(obj, price, request.REQUEST.get('quantity'))
    return HttpResponseRedirect(reverse('blocks.cart_detail'))
    
def cart_remove_item(request, queryset, object_id):
    obj = _get_object(queryset, object_id)
    cart = Cart(request)
    cart.remove(obj)
    return HttpResponseRedirect(reverse('blocks.cart_detail'))

def cart_checkout(request, queryset):
    pass

def cart_detail(request, queryset):
    return direct_to_template(request, template='blocks/cart_detail.html', extra_context={'cart':  Cart(request),})