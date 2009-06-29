from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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
    cart = Cart(request)
    if cart.get_items_count() > 0:
        user = request.user
        try:
            profile = user.get_profile()
            return direct_to_template(request, template='cart/checkout_confirm.html', extra_context={'cart': cart, 'profile': profile, })
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
    else:
        return HttpResponseRedirect(reverse('blocks.cart_detail'))
    
@login_required
def cart_confirm(request):
    cart = Cart(request)
    
    if cart.get_items_count() > 0:
        user = request.user
        profile = user.get_profile()
        current_site = Site.objects.get_current()
        context = { 'site': current_site, 'cart': cart, 'profile': profile }
        
        
        # send email to the user
        subject = render_to_string('cart/checkout_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('cart/checkout_email.txt', context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [profile.user.email])
        
        # send email to the shop manager
        subject = render_to_string('cart/checkout_manager_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('cart/checkout_manager_email.txt', context)
        recipient_list = ["%s <%s>" % mail_tuple for mail_tuple in settings.BLOCKS_SHOP_MANAGERS]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        
    
        cart.checkout(request)
        return direct_to_template(request, template='cart/checkout_complete.html')
    else:
        return HttpResponseRedirect(reverse('blocks.cart_detail'))

def cart_detail(request, queryset):
    return direct_to_template(request, template='cart/cart_detail.html', extra_context={'cart':  Cart(request),})