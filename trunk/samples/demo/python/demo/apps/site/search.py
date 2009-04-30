from blocks.apps.search import site, ModelSearch
from blocks.apps.search.fields import StripTagsField

from blocks.apps.core.models import StaticPage

class StaticPageSearch(ModelSearch):
    title = 'translation.title'
    fields = (
        StripTagsField('translation.body'),
    )

site.register(StaticPage, StaticPageSearch)
