from django import template
from blocks.apps.blog.models import BlogEntry

class BlogEntryListNode(template.Node):
    def __init__(self, varname, limit=10):
        self.varname = varname
        self.limit = limit

    def render(self, context):
        context[self.varname] = BlogEntry.objects.order_by('-publish_date')[:self.limit]
        return ''

def do_get_blog_list(parser, token):
    """
    {% get_blog_list as feed_list %}
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

# register tag on django
register = template.Library()
register.tag('get_blog_list', do_get_blog_list)