from blocks.apps.search.backends.base import SearchEngineBackend
from blocks.apps.search.query import RELEVANCE
from blocks.apps.search.results import SearchResults

class DummyBackend(BaseSearchEngine):
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def update(self, doc_id, model, fields, date):
        pass

    def remove(self, doc_id):
        pass

    def clear(self, models):
        pass

    def search(self, q, models=None, order_by=RELEVANCE, limit=None, offset=None):
        return SearchResults(q, [], 0, lambda r: r)