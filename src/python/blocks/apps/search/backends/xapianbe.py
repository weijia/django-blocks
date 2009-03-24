from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import smart_unicode

from blocks.apps.search.backends.base import SearchEngineBackend
from blocks.apps.search.query import RELEVANCE
from blocks.apps.search.results import SearchResults

from datetime import datetime
import unicodedata
import xapian

# Using Q as a UID prefix seems to be standard, undocumented practice in the
# xapian community
DOC_ID_TERM_PREFIX = 'Q'
DOC_ID_VALUE_INDEX = 0

def normalize_word(text):
    #text = text.lower()
    if isinstance(text, str):
        try:
            word = unicode(text,  sys.stdin.encoding)
        except UnicodeDecodeError:
            pass
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

class XapianBackend(SearchEngineBackend):
    """
    A search engine for local Xapian databases.
    """
    verbosity = 1
    
    def _read_only_db(self):
        """Retruns a read-only xapian Database object."""
        return xapian.Database(settings.BLOCKS_SEARH_INDEX_PATH)

    def _read_write_db(self):
        """Retruns a read-write xapian Database object."""
        return xapian.WritableDatabase(settings.BLOCKS_SEARH_INDEX_PATH, xapian.DB_CREATE_OR_OPEN)
    
    def update(self, doc_id, fields):
        doc = xapian.Document()
        doc.add_term(DOC_ID_TERM_PREFIX + doc_id)
        doc.add_value(DOC_ID_VALUE_INDEX, doc_id)
    
        db = self._read_write_db()
        
        indexer = xapian.TermGenerator()
        indexer.set_database(db)
        indexer.set_document(doc)
        #indexer.set_flags(xapian.TermGenerator.FLAG_SPELLING)

        #for field in fields:
        #    doc.add_term(field.name.lower())
    
        idx = 1
        for field in fields:
            if not field.value is None:
                value = normalize_word(smart_unicode(field.value))
                #doc.add_value(idx, value)
                indexer.index_text(value)
                indexer.index_text(value, 1, field.tag)
            idx = idx + 1
        
        # db.replace_document will create a new doc if a doc matching
        # doc_id is not found.
        xap_doc_id = db.replace_document(DOC_ID_TERM_PREFIX + doc_id, doc)
        
        # XXX: close the db, or make sure it runs in its own thread. Only
        # 1 writable connection can be open at a time.
        db.flush()
        del db

    def remove(self, doc_id):
        """Remove an object from its node."""
        # XXX: broken for now. obj._get_pk_val() is None once post_save is
        # sent. There is a message to django-dev regarding a fix for that.
        db.delete_document(DOC_ID_TERM_PREFIX + doc_id)

    def clear(self, models):
        pass

    def prep_value(self, db_field, value):
        """
        Hook to give the backend a chance to prep an attribute value before
        sending it to the search engine. By default, just return str(value).
        """
        # TODO: zero pad anything that should be treated as a number. xapian
        # only deals with strings for ordering, so we have to fake it.
        return str(value)

    def _result_callback(self, match):
        """
        Extract and return (app_label, model_name, pk, score) for the given
        xapian.Document.
        """
        guid = match.document.get_value(DOC_ID_VALUE_INDEX)
        app_label, model_name, pk_val = guid.split('://')[1].split('/')
        return (app_label, model_name, pk_val, match.percent)

    def search(self, query, models=None, order_by=RELEVANCE, limit=25, offset=0):
        db = self._read_only_db()
        
        # Start an enquire session.
        enquire = xapian.Enquire(db)
        
        # Parse the query string to produce a Xapian::Query object.
        qp = xapian.QueryParser()
        
        if models:
            for m in models:
                for field in m.fields:
                    qp.add_prefix(field.name.lower(), field.name.lower())
                    
        qp.set_default_op(xapian.Query.OP_OR)

        #stemmer = xapian.Stem("portuguese")
        #qp.set_stemmer(stemmer)
        qp.set_database(db)
        #qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        
        q = qp.parse_query(normalize_word(smart_unicode(query)))

        # Find the top 10 results for the query.
        enquire.set_query(q)
        matches = enquire.get_mset(offset, limit)
        
        if self.verbosity >= 2:
            print "query: %s" % q
            print "database total: %s" % db.get_doccount()
            print "matches size: %s" % matches.size()
        
        del db
        
        return SearchResults(query, matches, self._result_callback)
