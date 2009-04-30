from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from demo.apps.news.feeds import NewsFeed

admin.autodiscover()

urlpatterns = []

rss_feeds = {
    'news': NewsFeed,
}

# only serve static files if in a debug enviorment and the media url is relative
if settings.MEDIA_URL.startswith('/') and settings.DEBUG == True:
    media_url = settings.MEDIA_URL.strip('/')
    admin_media_url = settings.ADMIN_MEDIA_PREFIX.strip('/')
    urlpatterns += patterns('',
        (r'^%s/blocks/(?P<path>.*)$' % (media_url), 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_ROOT}),
        (r'^%s/(?P<path>.*)$' % (media_url), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'path': 'img/favicon.ico'}),
    )

urlpatterns += patterns('',

    # the sitemap
    #(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # localization
    (r'^i18n/', include('django.conf.urls.i18n')),

    # home page
    (r'^$', 'demo.apps.site.views.index'),

    # news
    url(r'^news/$',                  'demo.apps.news.views.list',   name="news.list"),
    url(r'^news/(?P<item_id>\d+)/$', 'demo.apps.news.views.detail', name="news.detail"),

    # rss feeds
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': rss_feeds}),
    
    # blocks - static pages
    (r'', include('blocks.apps.core.urls')),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # administration site
    url(r'^admin/(.*)', admin.site.root, name="admin.site.root"),
)
