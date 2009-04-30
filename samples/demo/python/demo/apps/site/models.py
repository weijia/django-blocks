from django.db import models
from django.utils.translation import ugettext_lazy as _

from blocks.apps.core import core_models
from blocks import forms

from tagging.fields import TagField
from tagging.models import Tag

#
# Image
#
class ArticleImage(models.Model):
    article = None

    image = forms.BlocksImageField(_('image'), upload_to='images', sizes=[('thumbnail', 96, 96), ('detail', 270, 173), ])
    description = models.CharField(_('description'), max_length=255)

    def __unicode__(self):
        return u'%s: %s' % (self.article, self.image.name)

    class Meta:
        abstract = True
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

class ArticleBaseModel(core_models.BaseContentModel):
        
    def _get_has_images(self):
        return self.images.count() > 0
    has_images = property(_get_has_images)

    def _get_image(self, index):
        try:
            return self.images.all()[index]
        except IndexError:
            return None

    def _get_thumbnail_url(self, index = 0):
        image = self._get_image(index)
        if image:
            return image.image.thumbnail.url()
        else:
            return ""
    thumbnail_url = property(_get_thumbnail_url)

    def _get_detail_url(self, index = 0):
        image = self._get_image(index)
        if image:
            return image.image.detail.url()
        else:
            return ""
    detail_url = property(_get_detail_url)

    def _get_image_url(self, index = 0):
        image = self._get_image(index)
        if image:
            return image.image.url
        else:
            return ""
    image_url = property(_get_image_url)

    def _get_image_description(self, index = 0):
        image = self._get_image(index)
        if image:
            return image.description
        else:
            return ""
    image_description = property(_get_image_description)

    def _get_image_list(self):
        return self.images.all()
    image_list = property(_get_image_list)

    class Meta:
        abstract = True

class ArticleModel(ArticleBaseModel):
    srcname = models.CharField(_('source'), help_text=_("source (ex: linuxfoundation)"), max_length=200, null=True, blank=True)
    srcurl = models.URLField(_('source URL'), help_text=_("source URL (ex: http://example.org/news/123/)"), verify_exists=False, max_length=200, null=True, blank=True)

    tag_list = TagField(_('tag list'), help_text=_('tags for this entry'), null=True, blank=True)
    
    def _get_tags(self):
        return Tag.objects.get_for_object(self)
    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)
    tags = property(_get_tags, _set_tags)
    
    class Meta:
        abstract = True