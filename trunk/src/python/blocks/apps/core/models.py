from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from blocks.apps.core import core_models
from blocks.apps.core.managers import BaseManager

from itertools import chain


#
# Menus
#
class MenuItem(core_models.BaseModel):
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)
    relurl = models.CharField(_('URL'), max_length=200, blank=False, 
            help_text=_("url relative to parent menu"))
    url = models.CharField(max_length=200, editable=False)
    level = models.IntegerField(_('Level'), default=0, editable=False)
    rank = models.IntegerField(_('Rank'), default=0, editable=False)
    menu = models.ForeignKey('Menu', related_name='contained_items', verbose_name=_('Menu'), null=True, blank=True, editable=False)

    def save(self, force_insert=False, force_update=False):
        from blocks.apps.core.menus import clean_ranks
        from blocks.core.utils import fix_url
        from django.template.defaultfilters import slugify   
        
        parts = self.relurl.split('/')
        parts = [slugify(p.replace(' ', '')) for p in parts]
        
        self.relurl = '/'.join(parts)
        self.relurl = fix_url(self.relurl)
        
        # Calculate level
        old_level = self.level
        if self.parent:
            self.level = self.parent.level + 1
            self.url = self.parent.url[:-1] + self.relurl
        else:
            self.level = 0
            self.url = self.relurl       

        if self.pk:
            old = MenuItem.objects.get(pk=self.pk)            
            new_parent = self.parent
            old_parent = old.parent
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
                
            if self.url != old.url:
                try:
                    p = StaticPage.objects.get(menu=old.url)
                    p.menu = self.url
                    p.save()
                except StaticPage.DoesNotExist:
                    pass

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
        from blocks.apps.core.menus import clean_ranks
        old_parent = self.parent
        super(MenuItem, self).delete()
        if old_parent:
            clean_ranks(old_parent.children())

    def name_with_spacer(self):
        spacer = ''
        for i in range(1, self.level):
            spacer += u'. . . '
        #if self.level > 0:
        #    spacer += u'. '
        return spacer + self.name

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


class MenuItemTranslation(core_models.BaseContentTranslation):
    model = models.ForeignKey(MenuItem, related_name="translations")

    caption = models.CharField(_('Caption'), max_length=100)
    description = models.CharField(_('Description'), max_length=200, blank=True)

    class Meta:
        db_table = 'blocks_menu_item_translation'


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


#
# Pages
#
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


class StaticPage(core_models.BaseContentModel):
    menu = models.CharField(_('URL'), max_length=100, choices=(), blank=False)

    relative = models.BooleanField(_('relative'),
      help_text=_("If a page is relative then the page slug (normalized name) is appended to the url."))

    template = models.ForeignKey(Template, verbose_name=_('template'), related_name='template_id', blank=False,
        help_text=_("You must provide a template to be used in this page."))

    slug = models.SlugField(_('slug'), editable=False)
    url = models.CharField(max_length=255, unique=True, editable=False)


    objects = BaseManager()
    
    def get_url(self):
        return self.menu if not self.relative else "%s%s/" % (self.menu, self.slug)

    def save(self, force_insert=False, force_update=False):
        from django.template.defaultfilters import slugify   
        self.slug = slugify(self.name)
        self.url = self.get_url()
        super(StaticPage, self).save(force_insert, force_update)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.name)

    def get_absolute_url(self):
        return self.url

    def _get_lead(self):
        s1 = self._get_body()
        i = s1.find('</p>')
        if i == -1:
            i = s1.find('<br>')
        s2 = s1[:i + 4] if i != -1 else s1
        return mark_safe(s2)
    lead = property(_get_lead)

    def _get_text(self):
        s1 = self._get_body()
        s2 = self._get_lead()
        if len(s1) != len(s2):
            s1 = s1[len(s2) + 4:]
        else:
            s1 = ""
        return mark_safe(s1)
    text = property(_get_text)

    def _get_body(self):
        return mark_safe(self.translation.body)
    body = property(_get_body)

    def _get_has_images(self):
        return self.images.count() > 0
    has_images = property(_get_has_images)

    def _get_image_list(self):
        return self.images.all()
    image_list = property(_get_image_list)

    class Meta:
        db_table = 'blocks_static_page'
        verbose_name = _('Static Page')
        verbose_name_plural = _('Static Pages')
        ordering = ('url',)


class StaticPageTranslation(core_models.BaseContentTranslation):
    model = models.ForeignKey(StaticPage, related_name="translations")

    title = models.CharField(_('title'), max_length=200)
    body = models.TextField(_('body'))

    def _get_lead(self):
        s1 = self.body
        i = s1.find('</p>')
        if i == -1:
            i = s1.find('<br>')
        s2 = s1[:i + 4] if i != -1 else s1
        return mark_safe(s2)
    lead = property(_get_lead)
    
    class Meta:
        db_table = 'blocks_static_page_translation'
        verbose_name = _('Static Page Translation')
        verbose_name_plural = _('Static Page Translations')
        ordering = ('id',)

class StaticPageImage(core_models.Image):
    article = models.ForeignKey(StaticPage, related_name="images")

    class Meta:
        db_table = 'blocks_static_page_image'
        verbose_name = _('Static Page Image')
        verbose_name_plural = _('Static Page Images')