import os
from django.conf import settings


if not settings.TEMPLATE_DIRS:
    settings.TEMPLATE_DIRS = []
settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), "templates"),)

#if not settings.BLOCKS_ADMIN_HELP:
settings.BLOCKS_ADMIN_HELP = {
'auth': {
    '__help__':     'Manage your site\'s users, groups and access to site features.',
    'group':        'Determine access to features by selecting permissions for groups.',
    'user':         'List, add, and edit users.'
    },
    
'blocks': {
    '__help__':     'Control how your site looks and feels. ',
    'page':        '',
    'staticpage':  'If you want to add a static page, like a contact page or an about page, use a page.',
    'template':    'Configure templates wich controls how content appears in your site.',
    'view':        'Views are customized lists of content on your system; they are highly configurable and give you control over how lists of content are presented.'
    },
}