from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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

@login_required
def cart_checkout(request):
    user = request.user
    try:
        profile = user.get_profile()
        return direct_to_template(request, template='cart/checkout_confirm.html', extra_context={'cart':  Cart(request), 'profile': profile, })
    except ObjectDoesNotExist:
        from profiles import utils
        
        form_class = utils.get_profile_form()
        if request.method == 'POST':
            form = form_class(data=request.POST, files=request.FILES)
            if form.is_valid():
                profile_obj = form.save(commit=False)
                profile_obj.user = request.user
                profile_obj.save()
                if hasattr(form, 'save_m2m'):
                    form.save_m2m()
                return HttpResponseRedirect(reverse('blocks.cart_checkout'))
        else:
            form = form_class()
        return direct_to_template(request, template='cart/checkout_needsprofile.html', extra_context={'form':  form,})

@login_required
def cart_confirm(request):
    cart = Cart(request)
    cart.checkout(request)
    return direct_to_template(request, template='cart/checkout_complete.html')

def cart_detail(request, queryset):
    return direct_to_template(request, template='cart/cart_detail.html', extra_context={'cart':  Cart(request),})