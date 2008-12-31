from django.db import models
from django.contrib import admin
#from django.core import validators
from base import STATUS_CHOICES, WEIGHT_CHOICES, LEVEL_CHOICES, _
from blocks.apps.wiki import wiki
from blocks.apps.core import core_models
from blocks.core import utils
from blocks import forms
import datetime

from itertools import chain
from django.core.exceptions import ObjectDoesNotExist

class Image(models.Model):
    image = forms.BlocksImageField(_('image'), upload_to='images/%Y/%m/%d', thumbnail_size=(96, 96))
    description = models.TextField(_('description'), max_length=255)

    class Meta:
        db_table = 'blocks_image'

class ImageAdmin(admin.ModelAdmin):
    search_fields = ('image', 'description')
    list_display = ('image', 'description')

admin.site.register(Image, ImageAdmin)

class Template(models.Model):
    name = models.CharField(_('name'), max_length=80, unique=True)
    description = models.CharField(_('description'), max_length=255)
    
    template = models.CharField(_('template'), max_length=70,
                    help_text=_("Example: 'homepage.html'. If this isn't provided, the system will use 'default.html'."))

    def delete(self):
        # TODO: validate if is system Template
        if self.name == "Default":
          return
        else:
          super(Template, self).delete()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        db_table = 'blocks_template'


class TemplateAdmin(admin.ModelAdmin):
    search_fields = ('template', 'name', 'description')
    list_display = ('name', 'template', 'description')

admin.site.register(Template, TemplateAdmin)


class StaticPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, unique=True, 
        help_text=_("Example: '/about/'. A leading and trailing slashes will be putted automaticly."))
    # content
    title = models.CharField(_('title'), max_length=200)
    body_wiki = models.TextField(_('body'),
         help_text=_("use reStructuredText Markup."))
    
    template = models.ForeignKey(Template, verbose_name=_('template'), related_name='template_id', blank=False,
        help_text=_("You must provide a template to be used in this page."))
    
    # publishing options
    publish_date = models.DateTimeField(_('publish date'), blank=True)
    modified_date = models.DateTimeField(_('modified date'), blank=True)
    author = models.CharField(_('author'), max_length=80, blank=True)
    
    def _get_body(self):
        return wiki.parse(self.body_wiki)    
    body = property(_get_body)
    
    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
    
    def save(self):
        from blocks.core.utils import fix_url
        self.url = fix_url(self.url)
        
        if not self.author:
            user = utils.get_current_user()
            author = ''
            try:
                if user.first_name or user.last_name:
                    author = (user.first_name + ' ' + user.last_name).strip()
                elif user.username:
                    author = user.username.strip()
            except AttributeError:
                pass
            
            if author:
                self.author = author
            else:
                self.author = 'anonymous'
        if not self.publish_date:
            self.publish_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        super(StaticPage, self).save()
        
    class Meta:
        db_table = 'blocks_static_page'
        verbose_name = _('Static Page')
        verbose_name_plural = _('Static Pages')
        ordering = ('url',)

class StaticPageAdmin(admin.ModelAdmin):    
    fieldsets = (
       (None,                    {'fields': ('title', 'body_wiki')}),
       (_('Display options'),    {'fields': ('url', 'template',),}),
       (_('Publishing options'), {'fields': ('publish_date', 'modified_date', 'author'), 'classes': ('collapse', )}),
    )
    list_filter = ('template', 'author')
    search_fields = ('template', 'title',)
    list_display = ('url', 'title', 'author', 'modified_date',)

admin.site.register(StaticPage, StaticPageAdmin)


class MenuItem(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)
    caption = models.CharField(_('Caption'), max_length=50)
    url = models.CharField(_('URL'), max_length=200, blank=True)
    named_url = models.CharField(_('Named URL'), max_length=200, blank=True)
    level = models.IntegerField(_('Level'), default=0, editable=False)
    rank = models.IntegerField(_('Rank'), default=0, editable=False)
    menu = models.ForeignKey('Menu', related_name='contained_items', verbose_name=_('Menu'), null=True, blank=True, editable=False)

    def __unicode__(self):
        return self.caption

    def save(self, force_insert=False, force_update=False):
        from treemenus.utils import clean_ranks

        # Calculate level
        old_level = self.level
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0

        if self.pk:
            new_parent = self.parent
            old_parent = MenuItem.objects.get(pk=self.pk).parent
            if old_parent != new_parent:
                #If so, we need to recalculate the new ranks for the item and its siblings (both old and new ones).
                if new_parent:
                    clean_ranks(new_parent.children()) # Clean ranks for new siblings
                    self.rank = new_parent.children().count()
                super(MenuItem, self).save(force_insert, force_update) # Save menu item in DB. It has now officially changed parent.
                if old_parent:
                    clean_ranks(old_parent.children()) # Clean ranks for old siblings
            else:
                super(MenuItem, self).save(force_insert, force_update) # Save menu item in DB

        else: # Saving the menu item for the first time (i.e creating the object)
            if not self.has_siblings():
                # No siblings - initial rank is 0.
                self.rank = 0
            else:
                # Has siblings - initial rank is highest sibling rank plus 1.
                siblings = self.siblings().order_by('-rank')
                self.rank = siblings[0].rank + 1
            super(MenuItem, self).save(force_insert, force_update)

        # If level has changed, force children to refresh their own level
        if old_level != self.level:
            for child in self.children():
                child.save() # Just saving is enough, it'll refresh its level correctly.

    def delete(self):
        from treemenus.utils import clean_ranks
        old_parent = self.parent
        super(MenuItem, self).delete()
        if old_parent:
            clean_ranks(old_parent.children())

    def caption_with_spacer(self):
        spacer = ''
        for i in range(0, self.level):
            spacer += u'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        if self.level > 0:
            spacer += u'|-&nbsp;'
        return spacer + self.caption

    def get_flattened(self):
        flat_structure = [self]
        for child in self.children():
            flat_structure = chain(flat_structure, child.get_flattened())
        return flat_structure

    def siblings(self):
        if not self.parent:
            return MenuItem.objects.none()
        else:
            if not self.pk: # If menu item not yet been saved in DB (i.e does not have a pk yet)
                return self.parent.children()
            else:
                return self.parent.children().exclude(pk=self.pk)

    def has_siblings(self):
        return self.siblings().count() > 0

    def children(self):
        _children = MenuItem.objects.filter(parent=self).order_by('rank',)
        for child in _children:
            child.parent = self # Hack to avoid unnecessary DB queries further down the track.
        return _children

    def has_children(self):
        return self.children().count() > 0

    class Meta:
        db_table = 'blocks_menu_item'


class Menu(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    root_item = models.ForeignKey(MenuItem, related_name='is_root_item_of', verbose_name=_('Root Item'), null=True, blank=True, editable=False)
    
    def save(self, force_insert=False, force_update=False):
        if not self.root_item:
            root_item = MenuItem()
            root_item.caption = _('Root')
            if not self.pk: # If creating a new object (i.e does not have a pk yet)
                super(Menu, self).save() # Save, so that it gets a pk
            root_item.menu = self
            root_item.save() # Save, so that it gets a pk
            self.root_item = root_item
        super(Menu, self).save(force_insert, force_update)

    def delete(self):
        if self.root_item is not None:
            self.root_item.delete()
        super(Menu, self).delete()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'blocks_menu'
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
