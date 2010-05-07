# -*- coding: utf-8 -*-
# $Id$
#
#
from django.contrib import admin
from blocks.apps.shop.admin import BaseAssetAdmin
from demo.apps.catalog.models import Product, Category

class CategoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(BaseAssetAdmin):
	pass

admin.site.register(Product, ProductAdmin)