from django.template import loader, RequestContext
from django.http import HttpResponse

from tagging.models import TaggedItem
from models import BlogEntry


def entries_bytag(request, tag, page=1):
	
	entries = TaggedItem.objects.get_by_model(BlogEntry, tag)

	t = loader.get_template("blog/blogentry_bytag.html")
	
	c = RequestContext(request, {'blog_list': entries, 'tag': tag })
	
	response = HttpResponse(t.render(c))
	return response