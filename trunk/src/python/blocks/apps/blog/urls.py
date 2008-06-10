from django.conf.urls.defaults import *
from models import BlogEntry

info_dict = {
    'queryset': BlogEntry.objects.all(),
    'date_field': 'publish_date',
    'num_latest': 10,
}

urlpatterns = patterns('django.views.generic.date_based',
 #  (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', 'object_detail', dict(info_dict, slug_field='slug')),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', info_dict),
   (r'^(?P<year>\d{4})/$', 'archive_year', info_dict),
   (r'^/?$', 'archive_index', info_dict),
)