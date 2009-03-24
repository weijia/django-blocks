from django.db.models.base import ModelBase
from blocks.apps.search.options import ModelSearch

class AlreadyRegistered(Exception):
    pass

class SearchSite(object):
    """
    An SearchSite object encapsulates an instance of the Django search application. 
    Models are registered with the SearchSite using the register() method.
    """
    
    def __init__(self):
        self._registry = {} # model_class class -> search_class instance
        
    def register(self, model_or_iterable, options_class=None, *args, **kwargs):
        """
        Registers the given model(s) with the given search class.
        
        The model(s) should be Model classes, not instances.
        
        If an search class isn't given, it will use ModelSearch (the default
        search options).
        
        If a model is already registered, this will raise AlreadyRegistered.
        """
        
        if not options_class:
            options_class = ModelSearch
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)
            
            options = options_class(model, self, *args, **kwargs)
            
            #if hasattr(model, 'indexer') is None:
            #    model.add_to_class('indexer', Indexer(model, options))
            
            # Instantiate the search class to save in the registry
            self._registry[model] = options
    
    def get_registered_models(self):
        return self._registry.iteritems()
    
# This global object represents the default search site, for the common case.
site = SearchSite()