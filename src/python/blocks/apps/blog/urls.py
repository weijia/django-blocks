from django.conf.urls.defaults import *
from models import BlogEntry

info_dict = {
    'queryset': BlogEntry.objects.all(),
    'date_field': 'publish_date',
}

idx_info_dict = {
    'queryset': BlogEntry.objects.all(),
    'template_name': 'blog/blogentry_archive.html',
    'template_object_name': 'latest',
    'paginate_by': 8,
}

#feeds = { 'rss': LatestBlogEntriesFeed, }

urlpatterns = patterns('',

   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/(?P<slug>[\d]+)/$', 'django.views.generic.date_based.object_detail', dict(info_dict, slug_field='id'), 'blog-details'),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$', 'django.views.generic.date_based.archive_day', info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'django.views.generic.date_based.archive_month', info_dict),
   (r'^(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year', info_dict),
   url(r'^$', 'django.views.generic.list_detail.object_list', idx_info_dict, 'blog-index'),
   
   #(r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)