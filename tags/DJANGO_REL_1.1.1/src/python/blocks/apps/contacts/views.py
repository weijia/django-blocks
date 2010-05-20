from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

def contacts_handler(request):
	if request.method == 'POST':
		
		key = 'default'
		
		items = []
		labels = {}
		for item in request.POST:
			if item[:2] == 'L[' and item[-1] == ']':
				labels[item[2:-1]] = request.POST[item]
			if item == 'EKEY':
				key = request.POST[item]
		for item in request.POST:
			value = request.POST[item]
			if not ((item[:2] == 'L[' and item[-1] == ']') or item == 'EKEY') and len(value) > 0:
				items.append({'name': labels[item] or item, 'value': value})
			   
		if len(items) > 0:
			current_site = Site.objects.get_current()
			context = { 'site': current_site, 'items': items, 'subject': labels["SUBJECT"] }
			
			# send email to the shop manager
			subject = render_to_string('contacts/email_subject.txt', context)
			subject = ''.join(subject.splitlines())
			message = render_to_string('contacts/email_message.txt', context)
			recipient_list = [mail for mail in settings.BLOCKS_CONTACT_MANAGERS[key]]
			#recipient_list = ["%s <%s>" % mail_tuple for mail_tuple in settings.BLOCKS_CONTACT_MANAGERS]
			send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
			
			return HttpResponseRedirect(reverse('blocks.contacts_success'))
		
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
	

def contacts_success(request):
	return direct_to_template(request, template='contacts/contact_success.html')
