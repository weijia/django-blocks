from django.conf.urls.defaults import url, patterns, include
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail, archive_day, archive_month, archive_year

from blocks.apps.blog.views import entries_bytag
from blocks.apps.blog.models import BlogEntry
#from blocks.apps.blog.feeds import LatestEntries

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

#feeds = { 'rss': LatestEntries, }

urlpatterns = patterns('',

   url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$', object_detail, dict(info_dict, month_format='%m', slug_field='slug'), 'blog.details'),
   (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', archive_day, dict(info_dict, month_format='%m')),
   (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', archive_month, dict(info_dict, month_format='%m')),
   (r'^(?P<year>\d{4})/$', archive_year, info_dict),
   url(r'^$', object_list, idx_info_dict, 'blog.index'),
   
   (r'^tag/(?P<tag>[\w-]+)/$', entries_bytag), 
   (r'^tag/(?P<tag>[\w-]+)/page/(?P<page>\d+)/$', entries_bytag),

   #(r'^(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
   
   (r'^comments/', include('django.contrib.comments.urls')),
)