from django import template
from django.template.defaulttags import url
from django.template import Node, Variable

from blocks.apps.core.models import Menu, MenuItem, StaticPage

register = template.Library()

def show_menu(context, menu_name, menu_type=None):
	try:
		menu = Menu.objects.get(name=menu_name)
		childs = menu.root_item.children()
		context['menus'] = childs if len(childs) > 0 else None
		context['menu_type'] = menu_type
	except:
		pass
	return context
register.inclusion_tag('blocks/menu.html', takes_context=True)(show_menu)

def show_sub_menu(context, menu_name, url, menu_type=None):
	try:
		if isinstance(menu_name, str) or isinstance(menu_name, unicode):
			menu = MenuItem.objects.filter(menu__name=menu_name, url=url)[0]
		else:
			menu = menu_name
		childs = menu.children()
		context['menus'] = childs if len(childs) > 0 else None
		context['menu_type'] = menu_type
	except:
		pass
	return context
register.inclusion_tag('blocks/menu_submenu.html', takes_context=True)(show_sub_menu)

def show_menu_item(context, menu_item, menu_type=None):
	context['menu_item'] = menu_item
	context['menu_type'] = menu_type
	return context
register.inclusion_tag('blocks/menu_item.html', takes_context=True)(show_menu_item)



class GetMenuNode(Node):
	def __init__(self, menu, url, varname):
		self.menu = Variable(menu)
		self.url = Variable(url)
		self.varname = varname

	def render(self, context):
		menu = self.menu.resolve(context)
		url = self.url.resolve(context)
		try:
			context[self.varname] = MenuItem.objects.get(menu__name=menu, url=url)
		except:
			pass
		return ''

def get_menu(parser, token):
	"""
	{% menu MENU_NAME in MENU_URL as MENU_ITEM_NAME %}
	"""
	bits = token.contents.split()
	if len(bits) != 6:
		raise template.TemplateSyntaxError, "'%s' tag takes 5 arguments" % bits[0]
	if bits[2] != "in":
		raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'in'" % bits[0]
	if bits[4] != "as":
		raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]

	return GetMenuNode(bits[1], bits[3], bits[5])
register.tag('menu', get_menu)


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
		self.menu = Variable(menu)
		self.varname = varname

	def render(self, context):
		menu = self.menu.resolve(context)
		context[self.varname] = StaticPage.objects.published().filter(menu__exact=menu)
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


class MenuItemListNode(template.Node):
	def __init__(self, url, varname):
		self.url = Variable(url)
		self.varname = varname

	def render(self, context):
		try:
			menu = MenuItem.objects.get(url=self.url.resolve(context))
			if menu:
				context[self.varname] = menu.children()
		except:
			pass
		return ''

def do_menutitem_list(parser, token):
	"""
	{% menuitems in BLOCKS_FULL_URL as menu_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 5:
		raise template.TemplateSyntaxError, "'%s' tag takes five arguments" % bits[0]
	if bits[1] != "in":
		raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'in'" % bits[0]
	if bits[3] != "as":
		raise template.TemplateSyntaxError, "Forth argument to '%s' tag must be 'as'" % bits[0]

	return MenuItemListNode(bits[2], bits[4])

register.tag('menuitems', do_menutitem_list)

@register.filter
def startswith(value, arg):
	"""Usage, {% if value|starts_with:"arg" %}"""
	if isinstance(value, str) or isinstance(value, unicode):
		return value.startswith(arg)
	else:
		return False
	
@register.filter
def inlist(value, arg):
	return value in arg

@register.filter
def less(value, arg):
	return value > arg
