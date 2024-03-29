from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.admin.util import unquote
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch

from blocks.apps.core.models import *
from blocks.apps.core.menus import get_parent_choices, get_menus_choices, MenuItemChoiceField, move_item_or_clean_ranks
from blocks.apps.core.forms import StaticPageAdminForm, BaseContentAdminForm
from blocks.apps.core.managers import STATUS_DISABLED, STATUS_DRAFT, STATUS_PUBLISHED
import re

def make_published(modeladmin, request, queryset):
	queryset.update(status=STATUS_PUBLISHED)
make_published.short_description = _("Mark selected as published")


class BaseAdmin(admin.ModelAdmin):
	class Media:
		css = {"all": (
			"blocks/css/jquery-tabs.css", 
			"blocks/wymeditor/skins/default/skin.css",
			"blocks/css/wymeditor.css",
		)}
		js = (
			"blocks/js/jquery.js",
			"blocks/js/jquery-ui.js",
			
			#** WYSIWYG editor **
			"blocks/wymeditor/jquery.wymeditor.min.js",
			#"blocks/wymeditor/plugins/jquery.wymeditor.filebrowser.js",
			#"blocks/wymeditor/plugins/hovertools/jquery.wymeditor.hovertools.js",
			#"blocks/wymeditor/plugins/resizable/jquery.wymeditor.resizable.js",
			
			#** dialogs and utils**
			#"blocks/js/jquery.selectboxes.js",
			#"blocks/js/jquery.url.js",
			#"blocks/js/jquery.wysiwyg.js",
			#"blocks/js/jquery.blockUI.js",
			#"blocks/js/jquery.json.js",
			#"blocks/js/jquery.jsonrpc.js",
			#"blocks/js/jquery.htmlClean.js",
			
			#** WYSIWYG editor init **
			"blocks/js/lang.js",
		)


class BaseContentAdmin(BaseAdmin):	
	PUBLISHING_OPTIONS = (_('Publishing Options'), {'fields': ('publish_date', 'unpublish_date', 'promoted', 'status',), 'classes': ('collapse', )})
	PUBLISHING_OPTIONS_NPROM = (_('Publishing Options'), {'fields': ('publish_date', 'unpublish_date', 'status',), 'classes': ('collapse', )})
	fieldsets = (
	   (None,					{'fields': ('name',)}),
	   PUBLISHING_OPTIONS,
	)
	list_filter = ('status', 'promoted')
	search_fields = ('name',)
	list_display = ('name', 'creation_user', 'lastchange_date', 'status', 'promoted')
	actions = [make_published]


class MultiLanguageInline(admin.options.InlineModelAdmin):
	template = 'blocks/multilang.html'
	extra = len(settings.LANGUAGES) if settings.USE_I18N else 1
	max_num = len(settings.LANGUAGES) if settings.USE_I18N else 1

class MultiImageTabular(admin.options.InlineModelAdmin):
	template = 'blocks/imagetabular.html'


#
# Menus
#
class MenuItemTranslationInline(MultiLanguageInline):
	model = MenuItemTranslation

class MenuItemAdmin(BaseAdmin):
	''' This class is used as a proxy by MenuAdmin to manipulate menu items. It should never be registered. '''

	inlines = [MenuItemTranslationInline]

	def __init__(self, model, admin_site, menu):
		super(MenuItemAdmin, self).__init__(model, admin_site)
		self._menu = menu

	def delete_view(self, request, object_id, extra_context=None):
		if request.method == 'POST': # The user has already confirmed the deletion.
			# Delete and return to menu page
			ignored_response = super(MenuItemAdmin, self).delete_view(request, object_id, extra_context)
			return HttpResponseRedirect("../../../")
		else:
			# Show confirmation page
			return super(MenuItemAdmin, self).delete_view(request, object_id, extra_context)

	def save_model(self, request, obj, form, change):
		obj.menu = self._menu
		obj.save()

	def response_add(self, request, obj, post_url_continue='../%s/'):
		try:
			response = super(MenuItemAdmin, self).response_add(request, obj, post_url_continue)
		except NoReverseMatch:
			return HttpResponseRedirect("../../")
		
		if request.POST.has_key("_continue"):
			return response
		elif request.POST.has_key("_addanother"):
			return HttpResponseRedirect(request.path)
		elif request.POST.has_key("_popup"):
			return response
		else:
			return HttpResponseRedirect("../../")

	def response_change(self, request, obj):
		try:
			response = super(MenuItemAdmin, self).response_change(request, obj)
		except NoReverseMatch:
			return HttpResponseRedirect("../../")
		if request.POST.has_key("_continue"):
			return HttpResponseRedirect(request.path)
		elif request.POST.has_key("_addanother"):
			return HttpResponseRedirect("../add/")
		elif request.POST.has_key("_saveasnew"):
			return HttpResponseRedirect("../%s/" % obj._get_pk_val())
		else:
			return HttpResponseRedirect("../../")

	def get_form(self, request, obj=None, **kwargs):
		form = super(MenuItemAdmin, self).get_form(request, obj, **kwargs)
		choices = get_parent_choices(self._menu, obj)
		form.base_fields['parent'] = MenuItemChoiceField(choices=choices)
		return form


class MenuAdmin(admin.ModelAdmin):
	menu_item_admin_class = MenuItemAdmin
	
	def get_urls(self):
		from django.conf.urls.defaults import patterns, url
		from django.utils.functional import update_wrapper
		
		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)
		
		urls = super(MenuAdmin, self).get_urls()
		urlpatterns = patterns('',
			(r'^(?P<menu_pk>[-\w]+)/items/add/$', wrap(self.add_menu_item)),
			(r'^(?P<menu_pk>[-\w]+)/items/(?P<menu_item_pk>[-\w]+)/$', wrap(self.edit_menu_item)),
			(r'^(?P<menu_pk>[-\w]+)/items/(?P<menu_item_pk>[-\w]+)/delete/$', wrap(self.delete_menu_item)),
			(r'^(?P<menu_pk>[-\w]+)/items/(?P<menu_item_pk>[-\w]+)/history/$', wrap(self.history_menu_item)),
			(r'^(?P<menu_pk>[-\w]+)/items/(?P<menu_item_pk>[-\w]+)/move_up/$', wrap(self.move_up_item)),
			(r'^(?P<menu_pk>[-\w]+)/items/(?P<menu_item_pk>[-\w]+)/move_down/$', wrap(self.move_down_item)),
		)
		return urlpatterns + urls

	
	def get_object_with_change_permissions(self, request, model, obj_pk):
		''' Helper function that returns a menu/menuitem if it exists and if the user has the change permissions '''
		try:
			obj = model._default_manager.get(pk=obj_pk)
		except model.DoesNotExist:
			# Don't raise Http404 just yet, because we haven't checked
			# permissions yet. We don't want an unauthenticated user to be able
			# to determine whether a given object exists.
			obj = None
		if not self.has_change_permission(request, obj):
			raise PermissionDenied
		if obj is None:
			raise Http404('%s object with primary key %r does not exist.' % (model.__name__, escape(obj_pk)))
		return obj

	def add_menu_item(self, request, menu_pk):
		''' Custom view '''
		menu = self.get_object_with_change_permissions(request, Menu, menu_pk)
		menuitem_admin = self.menu_item_admin_class(MenuItem, self.admin_site, menu)
		return menuitem_admin.add_view(request, extra_context={ 'menu': menu })

	def edit_menu_item(self, request, menu_pk, menu_item_pk):
		''' Custom view '''
		menu = self.get_object_with_change_permissions(request, Menu, menu_pk)
		menu_item_admin = self.menu_item_admin_class(MenuItem, self.admin_site, menu)
		return menu_item_admin.change_view(request, menu_item_pk, extra_context={ 'menu': menu })

	def delete_menu_item(self, request, menu_pk, menu_item_pk):
		''' Custom view '''
		menu = self.get_object_with_change_permissions(request, Menu, menu_pk)
		menu_item_admin = self.menu_item_admin_class(MenuItem, self.admin_site, menu)
		return menu_item_admin.delete_view(request, menu_item_pk, extra_context={ 'menu': menu })

	def history_menu_item(self, request, menu_pk, menu_item_pk):
		''' Custom view '''
		menu = self.get_object_with_change_permissions(request, Menu, menu_pk)
		menu_item_admin = self.menu_item_admin_class(MenuItem, self.admin_site, menu)
		return menu_item_admin.history_view(request, menu_item_pk, extra_context={ 'menu': menu })

	def move_down_item(self, request, menu_pk, menu_item_pk):
		menu = self.get_object_with_change_permissions(request, Menu, menu_pk)
		menu_item = self.get_object_with_change_permissions(request, MenuItem, menu_item_pk)

		if menu_item.rank < menu_item.siblings().count():
			move_item_or_clean_ranks(menu_item, 1)
			msg = _('The menu item "%s" was moved successfully.') % force_unicode(menu_item)
		else:
			msg = _('The menu item "%s" is not allowed to move down.') % force_unicode(menu_item)
		request.user.message_set.create(message=msg)
		return HttpResponseRedirect('../../../')

	def move_up_item(self, request, menu_pk, menu_item_pk):
		menu = self.get_object_with_change_permissions(request, Menu, menu_pk)
		menu_item = self.get_object_with_change_permissions(request, MenuItem, menu_item_pk)

		if menu_item.rank > 0:
			move_item_or_clean_ranks(menu_item, -1)
			msg = _('The menu item "%s" was moved successfully.') % force_unicode(menu_item)
		else:
			msg = _('The menu item "%s" is not allowed to move up.') % force_unicode(menu_item)
		request.user.message_set.create(message=msg)
		return HttpResponseRedirect('../../../')

admin.site.register(Menu, MenuAdmin)


#
# Pages
#

class TemplateAdmin(admin.ModelAdmin):
	search_fields = ('template', 'name', 'description')
	list_display = ('name', 'template', 'description')

admin.site.register(Template, TemplateAdmin)


class StaticPageTranslationInline(MultiLanguageInline):
	model = StaticPageTranslation

class StaticPageImagesInline(MultiImageTabular):
	model = StaticPageImage
	extra = 2
	max_num = 5

class StaticPageAdmin(BaseContentAdmin):
	form = StaticPageAdminForm
	inlines = [StaticPageTranslationInline, StaticPageImagesInline]
	fieldsets = (
		(None,  {'fields': ('name', 'menu', 'relative', 'template')}),
		(_('Publishing Options'), {'fields': ('publish_date', 'unpublish_date', 'status',), 'classes': ('collapse', )}),
	)
	list_filter = ('status', 'promoted', )
	search_fields = ('name', 'url','status', 'promoted')
	list_display = ('name', 'url', 'status')
	
	def get_form(self, request, obj=None, **kwargs):
		from django.forms import ChoiceField
		form = super(StaticPageAdmin, self).get_form(request, obj, **kwargs)
		form.base_fields['menu'] =  ChoiceField(choices=get_menus_choices())
		return form

admin.site.register(StaticPage, StaticPageAdmin)
