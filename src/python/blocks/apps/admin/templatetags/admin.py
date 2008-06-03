from django import template
from django.template import resolve_variable
from django.db.models import loading

register = template.Library()

class get_admin_help(template.Node):
    def __init__(self, model_label):
        self.model_label = model_label

    def render(self, context):
        model = resolve_variable(self.model_label, context);        
        url = model['admin_url'].split('/')
        app = url[0];
        mod = url[1];
        
        try:
            models = loading.cache.app_models[app]
            m = models[mod]
            if (m):
                try:
                    return m.help_text
                except AttributeError:
                    return ''
        except KeyError:
            return ''
        return ''

class DoGetAdminHelp:
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) < 1:
            raise template.TemplateSyntaxError, "'%s' statements require one arguments" % self.tag_name
        
        return get_admin_help(tokens[1])

register.tag('get_admin_help', DoGetAdminHelp('get_admin_help'))