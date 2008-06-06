import os
from django.conf import settings
from django.utils.translation import ugettext as _

if not settings.TEMPLATE_DIRS:
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

#if not settings.BLOCKS_ADMIN_HELP:
settings.BLOCKS_ADMIN_HELP = {
'auth': {
    '__label__':    _('Authentication'),
    '__help__':     _('Manage your site\'s users, groups and access to site features.'),
    'group':        _('Determine access to features by selecting permissions for groups.'),
    'user':         _('List, add, and edit users.')
    },
    
'contenttypes': {
    '__label__':    _('Blocks'),
    '__help__':     _('Control how your site looks and feels.'),
    'page':         _('List, add and edit pages.'),
    'staticpage':   _('If you want to add a static page, like a contact page or an about page, use a page.'),
    'template':     _('Configure templates wich controls how content appears in your site.'),
    'view':         _('Views are customized lists of content on your system; they are highly configurable and give you control over how lists of content are presented.')
    },
    
'aggregator': {
    '__label__':    _('Feed Aggregator'),
    '__help__':     _('Manage your site\'s feeds.'),
    'feed':         _('Add you feeds here.'),
    },
}