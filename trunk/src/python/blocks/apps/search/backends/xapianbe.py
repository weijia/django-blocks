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
DOC_DT_VALUE_INDEX = 1
DOC_KEY_TERM_PREFIX = 'K'

DOC_DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def normalize_word(text):
    #text = text.lower()
    text = text.replace("\n", " ");
    text = text.replace("\r", "");
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
    db = None
    writable = False
    verbosity = 1
    
    def start(self):
        if self.db is None:
            if self.writable:
                self.db = self._read_write_db()
            else:
                self.db = self._read_only_db()
    
    def stop(self):
        # XXX: close the db, or make sure it runs in its own thread. Only
        # 1 writable connection can be open at a time.
        if self.verbosity > 1:
            print "flush and close database"
        if self.writable:
            self.db.flush()
        del self.db
        self.db = None
    
    def _read_only_db(self):
        """Retruns a read-only xapian Database object."""
        if self.verbosity > 1:
            print "open read only database in %s" % settings.BLOCKS_SEARH_INDEX_PATH
        return xapian.Database(settings.BLOCKS_SEARH_INDEX_PATH)

    def _read_write_db(self):
        """Retruns a read-write xapian Database object."""
        if self.verbosity > 1:
            print "open writable database in %s" % settings.BLOCKS_SEARH_INDEX_PATH
        return xapian.WritableDatabase(settings.BLOCKS_SEARH_INDEX_PATH, xapian.DB_CREATE_OR_OPEN)
    
    def _get_document(self, id):
        postlist = self.db.postlist(id)
        try:
            plitem = postlist.next()
        except StopIteration:
            raise KeyError("Unique term %r not found" % id)
        return self.db.get_document(plitem.docid)
    
    def update(self, doc_id, fields, model, date):
        doc = xapian.Document()
        full_doc_id = DOC_ID_TERM_PREFIX + doc_id
        doc.add_term(full_doc_id)
        doc.add_value(DOC_ID_VALUE_INDEX, doc_id)
        doc.add_value(DOC_DT_VALUE_INDEX, datetime.strftime(date.value, DOC_DT_FORMAT))
    
        if not self.writable:
            return
        
        indexer = xapian.TermGenerator()
        indexer.set_database(self.db)
        indexer.set_document(doc)
        #indexer.set_flags(xapian.TermGenerator.FLAG_SPELLING)

        #for field in fields:
        #    doc.add_term(field.name.lower())
        
        try:
            l_doc = self._get_document(full_doc_id)
            z = l_doc.get_value(DOC_DT_VALUE_INDEX)
            ldt = datetime.strptime(z, DOC_DT_FORMAT)
        except KeyError:
            if self.verbosity > 1:
                print "document id %s not found" % full_doc_id
            ldt = datetime(1900, 1, 1)       
        
        if ldt < date.value:
            if self.verbosity > 1:
                print "last change %s" % datetime.strftime(date.value, DOC_DT_FORMAT)
                print "last update %s" % datetime.strftime(ldt, DOC_DT_FORMAT)
        
            #key = DOC_KEY_TERM_PREFIX + "MODEL"
            #value = model._
            #indexer.index_text(value, 1, key)
            #if self.verbosity > 1:
            #    print "key %s:%s" % (key, value)
        
            if self.verbosity > 1:
                print "update %s" % full_doc_id
            idx = 1
            for field in fields:
                if not field.value is None:
                    value = normalize_word(smart_unicode(field.value))
                    #doc.add_value(idx, value)
                    indexer.index_text(value)
                    if field.key is not None:
                        key = DOC_KEY_TERM_PREFIX + field.key.upper()
                        indexer.index_text(value, 1, key)
                        if self.verbosity > 1:
                            print "key %s:%s" % (key, value)
                    else:
                        indexer.index_text(value, 1, field.tag)
                        if self.verbosity > 1:
                            print "%s -> %s" % (field.tag, value)
                idx = idx + 1
            
            # db.replace_document will create a new doc if a doc matching
            # doc_id is not found.
            xap_doc_id = self.db.replace_document(full_doc_id, doc)
        
        elif self.verbosity > 1:
            print "document id %s not changed" % full_doc_id
        
        if self.verbosity > 1:
            print "----------------------------------------"

    def remove(self, doc_id):
        """Remove an object from its node."""
        # XXX: broken for now. obj._get_pk_val() is None once post_save is
        # sent. There is a message to django-dev regarding a fix for that.
        self.db.delete_document(DOC_ID_TERM_PREFIX + doc_id)

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
        pk_val, qs = pk_val.split('?')
        keys = [k.split('=') for k in qs.split('&')] if qs != '' else []
        return (app_label, model_name, pk_val, keys, match.percent)

    def search(self, query, models, order_by=RELEVANCE, limit=25, offset=0):        
        # Start an enquire session.
        enquire = xapian.Enquire(self.db)
        
        # Parse the query string to produce a Xapian::Query object.
        qp = xapian.QueryParser()
        
        for m in models:
            print m.fields
            for field in m.fields:
                if field.key is not None:
                    key = DOC_KEY_TERM_PREFIX + field.key.upper()
                    qp.add_boolean_prefix(field.key, key)
                    if self.verbosity > 1:
                        print "key %s:%s" % (key, field.key)
        
        qp.set_default_op(xapian.Query.OP_OR)

        #stemmer = xapian.Stem("portuguese")
        #qp.set_stemmer(stemmer)
        qp.set_database(self.db)
        #qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        
        query = normalize_word(smart_unicode(query))
        q = qp.parse_query(query)
        
        if self.verbosity > 1:
            print "query %s" % query

        # Find the top 10 results for the query.
        enquire.set_query(q)
        matches = enquire.get_mset(offset, limit)
        
        if self.verbosity > 1:
            print "query: %s" % q
            print "database total: %s" % self.db.get_doccount()
            print "matches size: %s" % matches.size()
        
        return SearchResults(query, matches, self._result_callback)
