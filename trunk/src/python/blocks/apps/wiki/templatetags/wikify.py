from django import template
from blocks.apps.wiki import wiki

def wikify(content):
	return wiki.parse(content)    

# do not encode this is safe HTML
wikify.is_safe=True

# register filter on django
register = template.Library()
register.filter(wikify)