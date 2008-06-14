from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

def parse(content):
    try:
        import pygments_directive
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in wiki filter: The Python pygments library isn't installed."
        pass
        
    try:
        from docutils.core import publish_parts
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in wiki filter: The Python docutils library isn't installed."
        return force_unicode(value)
    else:
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(source=smart_str(content), writer_name="html4css1", settings_overrides=docutils_settings)
        return mark_safe(force_unicode(parts["fragment"]))

