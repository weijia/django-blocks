from django.conf import settings
from django.core.management.base import CommandError, BaseCommand
from django.core.exceptions import ImproperlyConfigured

from blocks.apps.search import site

from optparse import make_option
import time

class Command(BaseCommand):
    help = "query the search index..."
    
    requires_model_validation = False
    can_import_settings = False
	        
    def handle(self, *args, **options):
        from blocks.apps import search
        from blocks.apps.search import backend
        from django.utils.html import strip_tags
        from django.utils.text import truncate_words
        
        search.autodiscover()
        
        # Combine the rest of the command line arguments with spaces between
        # them, so that simple queries don't have to be quoted at the shell
        # level.
        query_string = " ".join(args)
        
        models = site.get_registered_models()
        smodels = [search_options for model, search_options in models if search_options.instanciate(None)]
        
        backend.verbosity = int(options.get('verbosity'))
        a = time.time()
        backend.start()
        results = backend.search(query_string, smodels)
        backend.stop()
        b = time.time()
        
        print "results in %.3f sec(s)" % ((b-a)*1000)
        for r in results:
            print "%i%%: %s" % (r.score, r.model.__name__)
            print "-> %s" % r.object.translation.title
            print "%s" % truncate_words(strip_tags(r.object.translation.lead), 10)
            print "%s" % r.object.translation.lead
            print ""