from django import template
from django.template import resolve_variable
from django.conf import settings
from django.utils.translation import ugettext as _

register = template.Library()

class get_app_label(template.Node):
    def __init__(self, app_label):
        self.app_label = app_label

    def render(self, context):
        app = resolve_variable(self.app_label, context);        
        
        try:
            help = settings.BLOCKS_ADMIN_HELP[app['name'].lower()]
            return _(help['__label__'])
        except KeyError:
            return _(app['name'])
        return _(app['name'])
    
class get_app_help(template.Node):
    def __init__(self, app_label):
        self.app_label = app_label

    def render(self, context):
        app = resolve_variable(self.app_label, context);        
        
        try:
            help = settings.BLOCKS_ADMIN_HELP[app['name'].lower()]
            return help['__help__']
        except KeyError:
            return ''
        return ''
    
class get_model_help(template.Node):
    def __init__(self, model_label):
        self.model_label = model_label

    def render(self, context):
        model = resolve_variable(self.model_label, context);        
        url = model['admin_url'].split('/')
        app = url[0];
        mod = url[1];
        
        try:
            helps = settings.BLOCKS_ADMIN_HELP[app]
            m = helps[mod]
            return m
        except KeyError:
            return ''
        return ''

class DoGetAppLabel:
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) < 1:
            raise template.TemplateSyntaxError, "'%s' statements require one arguments" % self.tag_name
        
        return get_app_label(tokens[1])
    
class DoGetAppHelp:
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) < 1:
            raise template.TemplateSyntaxError, "'%s' statements require one arguments" % self.tag_name
        
        return get_app_help(tokens[1])
    
class DoGetModelHelp:
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) < 1:
            raise template.TemplateSyntaxError, "'%s' statements require one arguments" % self.tag_name
        
        return get_model_help(tokens[1])

register.tag('get_app_label',  DoGetAppLabel('get_app_label'))
register.tag('get_app_help',   DoGetAppHelp('get_app_help'))
register.tag('get_model_help', DoGetModelHelp('get_model_help'))
