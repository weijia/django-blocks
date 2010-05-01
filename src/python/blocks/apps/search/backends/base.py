from django.utils.encoding import force_unicode
from blocks.apps.search.query import RELEVANCE

class SearchEngineBackend(object):
	"""
	Abstract search engine base class.
	"""
	def start(self):
		raise NotImplementedError
	
	def stop(self):
		raise NotImplementedError

	def update(self, doc_id, model, fields, date):
		raise NotImplementedError

	def remove(self, doc_id):
		raise NotImplementedError

	def clear(self, models):
		raise NotImplementedError

	def search(self, query, models=None, order_by=RELEVANCE, limit=None, offset=None):
		raise NotImplementedError

	def prep_value(self, db_field, value):
		"""
		Hook to give the backend a chance to prep an attribute value before
		sending it to the search engine. By default, just force it to unicode.
		"""
		return force_unicode(value)