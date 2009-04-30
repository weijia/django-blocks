from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list_detail import object_list

from demo.apps.news.models import NewsArticle
from django.contrib.admin.models import LogEntry

# home page
def index(request):
    t = loader.get_template('site/homepage.html')

    context = {
        'news_list':  NewsArticle.objects.published()[:4],
        'history':    LogEntry.objects.all()[:15],
    }
    c = RequestContext(request, context)
    return HttpResponse(t.render(c))
