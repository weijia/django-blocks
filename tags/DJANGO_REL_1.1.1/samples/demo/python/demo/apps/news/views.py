from django.views.generic.list_detail import object_list,object_detail

from demo.apps.news.models import *

def list(request):
	# promoted news
	n = NewsArticle.objects.promoted()
	highs = n[:1]
	high_ids = [it.id for it in highs]
	
	# first X news (without promoted)
	news = NewsArticle.objects.published()
	news = news.exclude(id__in=high_ids)
	
	context = {
		'high_list': highs,
		'other_list': news[4:][:5], # next 5 news without the first 4
	}
	return object_list(request, template_name='news/list.html', queryset=news[:4],  extra_context=context, allow_empty='True')

def detail(request, item_id):
	news = NewsArticle.objects.filter(id=item_id)	
	context = {
		'other_list': NewsArticle.objects.published().exclude(id=item_id)[:5],
	}
	return object_detail(request, template_name='news/detail.html', queryset=news, object_id=item_id, extra_context=context)
