from django.views.generic.list_detail import object_list,object_detail
from blocks.apps.aggregator.models import Feed, FeedItem

def feed_list(request, feed_id=None):
    if feed_id:
        feeds = FeedItem.objects.filter(feed=feed_id).order_by('-date_modified')
    else:
        feeds = FeedItem.objects.order_by('-date_modified')
    list = Feed.objects.all()
    return object_list(request, queryset=feeds, extra_context={'feed_list': list}, paginate_by=10, allow_empty='True')

def feed_detail(request, feed_id, item_id):
    feeds = FeedItem.objects.filter(feed=feed_id).order_by('-date_modified')
    list = Feed.objects.all()
    return object_detail(request, queryset=feeds, object_id=item_id, extra_context={'feed_list': list})