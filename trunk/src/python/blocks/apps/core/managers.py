from django.db.models import Manager, Q
from django.utils.translation import ugettext_lazy as _
from django.db.models import options
from django.db.models.query import QuerySet

from datetime import datetime

options.DEFAULT_NAMES += ('db_name',)


class MultiDBManager(Manager):
	def get_query_set(self):
		db_name = getattr(self.model._meta, 'db_name', None)
		return QuerySet(self.model, using=db_name)
	
	@staticmethod
	def get_db_connection(model):
		db_name = getattr(model._meta, 'db_name', None)
		if not db_name is None:
			from django.db import connections
			return connections[db_name]
		else:
			from django.db import connection
			return connection


STATUS_DRAFT	 = 'N'
STATUS_PUBLISHED = 'P'
STATUS_DISABLED  = 'D'

STATUS_CHOICES = (
	(STATUS_DRAFT,	 _('Draft')),
	(STATUS_PUBLISHED, _('Published')),
	(STATUS_DISABLED,  _('Disabled')),
)

class BaseManager(Manager):

	def published(self, request=None):
		# allow staff users to preview pages
		allow_unpublished  = (request and request.user.is_authenticated() and request.user.is_staff)	
		if allow_unpublished:
			return self.all()
		else:
			return self.filter(
				Q(unpublish_date__gte=datetime.now()) | Q(unpublish_date__isnull=True),
				publish_date__lte=datetime.now(),
				status=STATUS_PUBLISHED
			)

	def promoted(self):
		return self.published().filter(promoted=True)
