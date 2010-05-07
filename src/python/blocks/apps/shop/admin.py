# -*- coding: utf-8 -*-
# $Id$
#
# Blocks shop model admin

from django.contrib import admin
from django.contrib.contenttypes import generic

from blocks.apps.shop.models import Asset, AssetKind


class BaseAssetInline(generic.GenericTabularInline):
	"""
	"""
	model = Asset
	max_num = 1

class BaseAssetKindInline(generic.GenericTabularInline):
	"""
	"""
	model = AssetKind

class BaseAssetAdmin(admin.ModelAdmin):
	"""
	"""
	inlines = [
        BaseAssetInline,
		BaseAssetKindInline
    ]


