from django.db.models import Manager, Q, sql
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.transaction import savepoint_state
from django.db.models import options
from django.db.models.query import QuerySet
from django.db.models.sql import BaseQuery
from django.core import signals
		
from datetime import datetime

options.DEFAULT_NAMES += ('db_name',)

try:
	import thread
except ImportError:
	import dummy_thread as thread

_connections  = {}

# Register an event that closes the database connections
# when a Django request is finished.
def close_connection(**kwargs):
	global _connections
	for connection in _connections.itervalues():
		connection.close()
	_connections = {}
signals.request_finished.connect(close_connection)

class MultiDBManager(Manager):

	@staticmethod
	def get_db_connection(model):
		db_name = getattr(model._meta, 'db_name', None)
		if not db_name is None:
			if not _connections.has_key(db_name):
				from django.db import load_backend
				settings_dict = settings.DATABASES[db_name]
				backend = load_backend(settings_dict['DATABASE_ENGINE'])
				wrapper = backend.DatabaseWrapper(MultiDBManager._get_settings(settings_dict))
				wrapper._cursor()
				_connections[db_name] = wrapper
			return _connections[db_name]
		else:
			from django.db import connection
			return connection
	
	@staticmethod
	def _get_settings(settings_dict):
		return {
			'DATABASE_HOST': settings_dict.get('DATABASE_HOST'),
			'DATABASE_NAME': settings_dict.get('DATABASE_NAME'),
			'DATABASE_OPTIONS': settings_dict.get('DATABASE_OPTIONS') or settings.DATABASE_OPTIONS,
			'DATABASE_PASSWORD': settings_dict.get('DATABASE_PASSWORD'),
			'DATABASE_PORT': settings_dict.get('DATABASE_PORT'),
			'DATABASE_USER': settings_dict.get('DATABASE_USER'),
			'TIME_ZONE': settings.TIME_ZONE,
		}  
		
	def get_query_set(self):
		connection = MultiDBManager.get_db_connection(self.model)
		if connection.features.uses_custom_query_class:
			Query = connection.ops.query_class(BaseQuery)
		else:
			Query = BaseQuery
		qs = QuerySet(self.model, Query(self.model, connection))
		return qs
	
	def _insert(self, values, return_id=False, raw_values=False):
		query = sql.InsertQuery(self.model, self.get_db_wrapper())
		query.insert_values(values, raw_values)
		ret = query.execute_sql(return_id)
		query.connection._commit()
		thread_ident = thread.get_ident()
		if thread_ident in savepoint_state:
			del savepoint_state[thread_ident]
		return ret


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