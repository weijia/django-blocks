from django import template
from blocks.apps.contenttypes.models import Menu

class PrimaryMenus(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = Menu.objects.filter(level='P').order_by('weight')
        return ''
    
class SecondaryMenus(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = Menu.objects.filter(level='S').order_by('weight')
        return ''

def do_get_menu_list(parser, token):
    """
    {% get_meny_list primary as primary_list %}
    {% get_meny_list secondary as secondary_list %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    if bits[1] != "primary" and bits[1] != "secondary":
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'primary' or 'secondary'" % bits[0]
    if bits[2] != "as":
        raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]

    if bits[1] == "primary":
        return PrimaryMenus(bits[3])
    else:
        return SecondaryMenus(bits[3])

# register tag on django
register = template.Library()
register.tag('get_menu_list', do_get_menu_list)