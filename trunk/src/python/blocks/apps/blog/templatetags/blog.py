from django import template
from blocks.apps.blog.models import BlogEntry

class BlogEntryListNode(template.Node):
	def __init__(self, varname, limit=10):
		self.varname = varname
		self.limit = limit

	def render(self, context):
		context[self.varname] = BlogEntry.objects.published()[:self.limit]
		return ''

def do_get_blog_list(parser, token):
	"""
	{% get_blog_list as feed_list [limit 10] %}
	"""
	bits = token.contents.split()
	if len(bits) != 3 and len(bits) != 5:
		raise template.TemplateSyntaxError, "'%s' tag takes two or four arguments" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
	if len(bits) > 3 and bits[3] != "limit":
		raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'limit'" % bits[0]
	
	if len(bits) == 3:
		return BlogEntryListNode(bits[2])
	else:
		return BlogEntryListNode(bits[2], bits[4])

class BlogEntryPromotedListNode(template.Node):
	def __init__(self, varname, limit=10):
		self.varname = varname
		self.limit = limit

	def render(self, context):
		context[self.varname] = BlogEntry.objects.promoted()[:self.limit]
		return ''

def do_get_blog_promoted_list(parser, token):
	"""
	{% get_blog_promoted_list as feed_list [limit 10] %}
	"""
	bits = token.contents.split()
	if len(bits) != 3 and len(bits) != 5:
		raise template.TemplateSyntaxError, "'%s' tag takes two or four arguments" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
	if len(bits) > 3 and bits[3] != "limit":
		raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'limit'" % bits[0]
	
	if len(bits) == 3:
		return BlogEntryPromotedListNode(bits[2])
	else:
		return BlogEntryPromotedListNode(bits[2], bits[4])

class BlogEntryDatesListNode(template.Node):
	def __init__(self, varname, limit=10):
		self.varname = varname
		self.limit = limit

	def render(self, context):
		context[self.varname] = BlogEntry.objects.dates('publish_date', 'month')[:self.limit]
		return ''
	
def do_get_blog_dates(parser, token):
	"""
	{% get_blog_dates as dates_list [limit 10] %}
	"""
	bits = token.contents.split()
	if len(bits) != 3 and len(bits) != 5:
		raise template.TemplateSyntaxError, "'%s' tag takes two or four arguments" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
	if len(bits) > 3 and bits[3] != "limit":
		raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'limit'" % bits[0]
	
	if len(bits) == 3:
		return BlogEntryDatesListNode(bits[2])
	else:
		return BlogEntryDatesListNode(bits[2], bits[4])


def tagweight(value):
	v = int(value)
	return ((v * 100) / 6) + (100 / v)



# register tag on django
register = template.Library()
register.tag('get_blog_list', do_get_blog_list)
register.tag('get_blog_promoted_list', do_get_blog_promoted_list)
register.tag('get_blog_dates', do_get_blog_dates)
register.filter(tagweight)

