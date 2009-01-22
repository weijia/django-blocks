from django import template
from django.template.defaulttags import url
from django.template import Node

from blocks.apps.core.models import Menu, MenuItem, StaticPage

register = template.Library()

def show_menu(context, menu_name, menu_type=None):
    menu = Menu.objects.get(name=menu_name)
    context['menu'] = menu
    if menu_type:
        context['menu_type'] = menu_type
    return context
register.inclusion_tag('blocks/menu.html', takes_context=True)(show_menu)


def show_menu_item(context, menu_item):
    if not isinstance(menu_item, MenuItem):
        raise template.TemplateSyntaxError, 'Given argument must be a MenuItem object.'

    context['menu_item'] = menu_item
    return context
register.inclusion_tag('blocks/menu_item.html', takes_context=True)(show_menu_item)


class ReverseNamedURLNode(Node):
    def __init__(self, named_url, parser):
        self.named_url = named_url
        self.parser = parser

    def render(self, context):
        from django.template import TOKEN_BLOCK, Token

        resolved_named_url = self.named_url.resolve(context)
        contents = u'url ' + resolved_named_url

        urlNode = url(self.parser, Token(token_type=TOKEN_BLOCK, contents=contents))
        return urlNode.render(context)


def reverse_named_url(parser, token):
    bits = token.contents.split(' ', 2)
    if len(bits) !=2 :
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (named url)" % bits[0])
    named_url = parser.compile_filter(bits[1])

    return ReverseNamedURLNode(named_url, parser)
reverse_named_url = register.tag(reverse_named_url)



class StaticPageListNode(template.Node):
    def __init__(self, menu, varname):
        self.menu = menu
        self.varname = varname

    def render(self, context):
        context[self.varname] = StaticPage.objects.filter(menu__exact=context[self.menu])
        return ''

def do_staticpages_list(parser, token):
    """
    {% staticpages in BLOCKS_URL as page_list %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "'%s' tag takes four arguments" % bits[0]
    if bits[1] != "in":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'in'" % bits[0]
    if bits[3] != "as":
        raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]

    return StaticPageListNode(bits[2], bits[4])


register.tag('staticpages', do_staticpages_list)