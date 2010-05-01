from django.conf import settings
from django.core.management.base import CommandError, BaseCommand
from django.core.exceptions import ImproperlyConfigured

from optparse import make_option

class Command(BaseCommand):
	help = "Aggregates feeds..."

	requires_model_validation = False
	can_import_settings = False
			
	def handle(self, *args, **options):
	  from blocks.apps.aggregator.feedupdator import update_feeds
	  update_feeds(options.get('verbosity'))

