from django import template


def get_contents_tag(parser, token):
	"""
	{% get_contents as dates_list [limit 10] %}
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


# register tag on django
register = template.Library()
register.tag('get_contents', get_contents_tag)
