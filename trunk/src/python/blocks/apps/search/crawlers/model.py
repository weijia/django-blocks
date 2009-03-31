# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from blocks.apps.search.crawlers.base import Crawler
from blocks.apps.search import site

class ModelCrawler(Crawler):

    def crawl(self):
        models = site.get_registered_models()
        for model, search_options in models:
            #ct = ContentType.objects.get_for_model(model)
            for instance in search_options.manager.all():
                search_options.instanciate(instance)
                self.backend.update(search_options.guid, search_options.fields)
                