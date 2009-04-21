from django.conf import settings
from django.core.management.base import CommandError, BaseCommand
from django.core.exceptions import ImproperlyConfigured

from optparse import make_option
import os

if not hasattr(settings, "BLOCKS_SEARCH_CRAWLERS"):
    raise ImproperlyConfigured("You must define the BLOCKS_SEARCH_CRAWLERS setting before crawl in the search framework.")

def get_crawler(name):
	class_name = "%sCrawler" % name.split(".")[-1].capitalize()
	try:
	    # Most of the time, the search crawl will be one of the  
	    # crawlerers that ships with django-search, so look there first.
	    mod = __import__('blocks.apps.search.crawlers.%s' % name, {}, {}, class_name)
	    crawler = getattr(mod, class_name)
	except ImportError, e:
	    # If the import failed, we might be looking for a search crawl 
	    # distributed external to django-search. So we'll try that next.
	    try:
	        mod = __import__(name, {}, {}, class_name)
	        crawler = getattr(mod, class_name)
	    except ImportError, e_user:
	        # The database crawl wasn't found. Display a helpful error message
	        # listing all possible (built-in) database crawlers.
	        p = __import__('blocks.apps.search.crawlers', {}, {}, ['']).__path__[0]
	        
	        available_crawlers = [
	            os.path.splitext(f)[0] for f in os.listdir(p)
	            if f != "base.py"
	            and not f.startswith('_') 
	            and not f.startswith('.') 
	            and not f.endswith('.pyc')
	        ]
	        available_crawlers.sort()
	        if name not in available_crawlers:
	            raise ImproperlyConfigured, "%r isn't an available search crawlers. Available options are: %s" % \
	                (name, ", ".join(map(repr, available_crawlers)))
	        else:
	            raise # If there's some other error, this must be an error in Django itself.
	return crawler
	          
class Command(BaseCommand):
    help = "crawl and create/update search index..."
    
    requires_model_validation = True
    can_import_settings = False
            
    def load_crawlers(self, verbosity):
        from blocks.apps import search
        from blocks.apps.search import backend
        
        search.autodiscover()
        
        crawlers = []
        for crawler_path in settings.BLOCKS_SEARCH_CRAWLERS:
            crawler_class = get_crawler(crawler_path)
            if crawler_class is None:
            	raise ImproperlyConfigured, "%r isn't an available search crawlers." % crawler_class
            crawlers.append(crawler_class(backend, verbosity))
        return crawlers
	        
    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity'))
        crawlers = self.load_crawlers(verbosity)
        
        for crawler in crawlers:
            crawler.crawl()