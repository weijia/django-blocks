from django.conf.urls.defaults import url, patterns
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail, archive_day, archive_month, archive_year
from blocks.apps.blog.views import entries_bytag
from models import BlogEntry

info_dict = {
    'queryset': BlogEntry.objects.all(),
    'template_object_name': 'blog',
    'date_field': 'publish_date',
}

idx_info_dict = {
    'queryset': BlogEntry.objects.all(),
    'template_name': 'blog/blogentry_archive.html',
    'template_object_name': 'blog',
    'paginate_by': 8,
}

#feeds = { 'rss': LatestBlogEntriesFeed, }

urlpatterns = patterns('',

   url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/(?P<slug>[\d]+)/$', object_detail, dict(info_dict, slug_field='id'), 'blog.details'),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{1,2})/$', archive_day, info_dict),
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', archive_month, info_dict),
   (r'^(?P<year>\d{4})/$', archive_year, info_dict),
   url(r'^$', object_list, idx_info_dict, 'blog.index'),
   
   #(r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
   
    (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$', entries_bytag), 
    (r'^tag/(?P<tag>[-_A-Za-z0-9]+)/page/(?P<page>\d+)/$', entries_bytag),

)