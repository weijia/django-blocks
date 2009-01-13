import os.path
from django.db.models.fields.files import ImageField
from django.db.models import signals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from widgets import DelAdminFileWidget
from forms import BlocksImageFormField
import os, shutil

class ThumbnailField:
    '''
    Instances of this class will be used to access data of the
    generated thumbnails
    '''
    def __init__(self, name):
        self.name = name
        self.storage = FileSystemStorage()

    def path(self):
        return self.storage.path(self.name)

    def url(self):
        return self.storage.url(self.name)

    def size(self):
        return self.storage.size(self.name)

class BlocksImageField(ImageField):
    '''
    Django field that behaves as ImageField, with some extra features like:
        - Auto resizing
        - Automatically generate thumbnails
        - Allow image deletion
    '''

    FIT_CENTER = (0.5, 0.5)
    FIT_TLEFT  = (0.0, 0.0)
    FIT_TRIGHT = (0.0, 1.0)
    FIT_BLEFT  = (1.0, 0.0)
    FIT_BRIGHT = (1.0, 1.0)
    
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        params_size = ('name', 'width', 'height', 'fit')

        if sizes and (isinstance(sizes, tuple) or isinstance(sizes, list)):
            sz = []
            for size in sizes:
                sz.append(dict(map(None, params_size, size)))
            setattr(self, 'sizes', sz)
        else:
            setattr(self, 'sizes', None)
        super(BlocksImageField, self).__init__(verbose_name, name, width_field, height_field, **kwargs)

    def _get_thumbnail_filename(self, filename, name=None):
        '''
        Returns the thumbnail name associated to the standard image filename
            * Example: /var/www/myproject/media/img/1/original.jpg
                will return /var/www/myproject/media/img/1/thumbnail.jpg
        '''

        if not name:
            if self.sizes and len(self.sizes) > 0:
                name = self.sizes[0]['name']
            else:
                name = 'original'
        
        ext = os.path.splitext(filename)[1].lower()
        dir = os.path.dirname(filename)
        return os.path.join(dir, "%s%s" % (name, ext))

    def _resize_image(self, filename, size):
        '''
        Resizes the image to specified width, height and force option
        '''
        WIDTH, HEIGHT = 0, 1
        from PIL import Image, ImageOps
        img = Image.open(filename)
        if img.size[WIDTH] != size['width'] or img.size[HEIGHT] != size['height']:
            img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS, 0, BlocksImageField.FIT_CENTER)
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _create_sizes(self, instance=None, **kwargs):
        '''
        Renames the image, and calls methods to resize and create the other sizes
        '''
        field = getattr(instance, self.name, None)
        if field:
            filename = field.path

            ext = os.path.splitext(filename)[1].lower()
            dir = os.path.join(self.get_directory_name(), str(instance._get_pk_val()))
            dst = os.path.join(dir, '%s%s' % ('original', ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)

            if os.path.abspath(filename) != os.path.abspath(dst_fullpath):
                if os.path.exists(filename):
                    dir = os.path.join(settings.MEDIA_ROOT, dir)
                    if not os.path.exists(dir):
                        os.mkdir(dir)
                    os.rename(filename, dst_fullpath)

                    for size in self.sizes:
                        size_filename = self._get_thumbnail_filename(dst_fullpath, size['name'])
                        shutil.copyfile(dst_fullpath, size_filename)
                        self._resize_image(size_filename, size)

                setattr(instance, self.attname, dst)
                #instance.error()
                instance.save()


        pass

    def _init_sizes(self, instance=None, **kwargs):
        '''
        Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        '''
        field = getattr(instance, self.name, None)
        if field:
            for size in self.sizes:
                filename = self.storage.url( field.name )
                size_filename = self._get_thumbnail_filename(filename, size['name'])
                size_field = ThumbnailField(size_filename)
                setattr(field, size['name'], size_field)


    def formfield(self, **kwargs):
        '''
        Specify form field and widget to be used on the forms
        '''
        kwargs['widget'] = DelAdminFileWidget
        kwargs['form_class'] = BlocksImageFormField
        return super(BlocksImageField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        '''
            Overwrite save_form_data to delete images if "delete" checkbox
            is selected
        '''
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            dir = os.path.dirname(filename)
            if os.path.exists(dir):
                os.rmdir(dir)
        else:
            super(BlocksImageField, self).save_form_data(instance, data)

    def get_db_prep_save(self, value):
        '''
            Overwrite get_db_prep_save to allow saving nothing to the database
            if image has been deleted
        '''
        if value:
            return super(BlocksImageField, self).get_db_prep_save(value)
        else:
            return u''

    def contribute_to_class(self, cls, name):
        '''
        Call methods for generating all operations on specified signals
        '''
        super(BlocksImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._create_sizes, sender=cls)
        signals.post_init.connect(self._init_sizes,   sender=cls)
