# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from blocks.apps.search.crawlers.base import Crawler
from blocks.apps.search import site
from datetime import date

class ModelCrawler(Crawler):

    def crawl(self):
        models = site.get_registered_models()
        self.backend.writable = True
        self.backend.start()
        for model, search_options in models:
            #ct = ContentType.objects.get_for_model(model)
            for instance in search_options.manager.all():
                for lang in settings.BLOCKS_LANGUAGES:
                    self.set_language(lang[0])
                    if hasattr(search_options.date, 'value')  and isinstance(search_options.date.value, date):
                        self.backend.update(search_options.guid, search_options.fields, model, search_options.date)
        self.backend.stop()
    
    def set_language(self, lang):
        from django.utils.translation.trans_real import activate
        activate(lang)
                
