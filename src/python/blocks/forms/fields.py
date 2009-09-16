import os.path
from django.db.models import Field, TextField, ImageField, signals
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from widgets import DelAdminFileWidget, GeoLocationWidget
from forms import GeoLocationFormField, BlocksImageFormField
import shutil


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

    FIT_CENTER       = (0.5, 0.5)
    FIT_TOP_LEFT     = (0.0, 0.0)
    FIT_TOP_RIGHT    = (0.0, 1.0)
    FIT_BOTTOM_LEFT  = (1.0, 0.0)
    FIT_BOTTOM_RIGHT = (1.0, 1.0)
    FIT_ADD_BORDERS  = (-1, -1)

    MODE_OPTIONS = (
        (_('Center'), "FIT_CENTER"),
        (_('Top Left'), "FIT_TOP_LEFT"),
        (_('Top Right'), "FIT_TOP_RIGHT"),
        (_('Bottom Left'), "FIT_BOTTOM_LEFT"),
        (_('Bottom Right'), "FIT_BOTTOM_RIGHT"),
        (_('Add Borders (if needed)'), "FIT_ADD_BORDERS"),
    )
    
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        params_size = ('name', 'width', 'height', 'fit')
        self.mode = BlocksImageField.FIT_CENTER
        
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
        from PIL import Image
        from PIL import ImageOps
        from PIL import ImageDraw
        from PIL import ImageColor
        
        img = Image.open(filename)
        if img.size[WIDTH] != size['width'] or img.size[HEIGHT] != size['height']:
            
            if self.mode[0] == -1:
                im = img
                img = Image.new("RGBA", (size['width'], size['height']))
                dr = ImageDraw.Draw(img)
                
                # if is a jpeg just draw a white rectang
                if 'jfif' in im.info:
                    dr.rectangle([(-1, -1), (size['width'] + 1, size['height'] + 1)], ImageColor.getrgb("#fff"))
            
                im.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            
                x = (size['width']  - im.size[0]) / 2
                y = (size['height'] - im.size[1]) / 2
                
                img.paste(im, (x, y))
            else:
                img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS, 0, self.mode)
                
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _fixpath(self, path):
        """
        os.path.normcase:
        Normalize the case of a pathname. On Unix and Mac OS X, this returns the path unchanged; on case-insensitive
        filesystems, it converts the path to lowercase. On Windows, it also converts forward slashes to backward slashes.
        needed for Windows path comparing!!
        """
        return os.path.normcase(os.path.abspath(path))

    def _create_sizes(self, instance=None, **kwargs):
        '''
        Renames the image, and calls methods to resize and create the other sizes
        '''
        field = getattr(instance, self.name, None)
        if field:
            filename = self._fixpath(field.path)
            self.mode = getattr(instance, self.name + '___mode', BlocksImageField.FIT_CENTER)
            
            if self.mode is None: return
            
            ext = os.path.splitext(filename)[1].lower()
            dirname = os.path.join(self.get_directory_name(), str(instance._get_pk_val()))
            dst = os.path.join(dirname, '%s%s' % ('original', ext))
            dst_fullpath = self._fixpath(os.path.join(settings.MEDIA_ROOT, dst))

            if filename != dst_fullpath:
                if os.path.exists(filename):
                    dirname = os.path.join(settings.MEDIA_ROOT, dirname)
                    if not os.path.exists(dirname):
                        os.mkdir(dirname)
                    if os.path.isfile(dst_fullpath):
                        os.remove(dst_fullpath)
                    os.rename(filename, dst_fullpath)
                setattr(instance, self.attname, dst)
                instance.save()

            if os.path.exists(filename):                
                size_filename = self._get_thumbnail_filename(dst_fullpath, "thumbnail_adm")
                shutil.copyfile(dst_fullpath, size_filename)
                self._resize_image(size_filename, {'width': 70, 'height': 50})
                
                for size in self.sizes:
                    size_filename = self._get_thumbnail_filename(dst_fullpath, size['name'])
                    shutil.copyfile(dst_fullpath, size_filename)
                    self._resize_image(size_filename, size)

    def _delete_sizes(self, instance=None, **kwargs):
        field = getattr(instance, self.name, None)
        if field:
            filename = self.storage.url( field.name )
            for size in self.sizes:
                delattr(field, size['name'])
            dirname = os.path.dirname(field.path)
            #if os.path.exists(dirname):
            #    shutil.rmtree(dirname, True)
                
    def _init_sizes(self, instance=None, **kwargs):
        '''
        Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        '''
        field = getattr(instance, self.name, None)
        if field:
            filename = self.storage.url( field.name )
            size_filename = self._get_thumbnail_filename(filename, "thumbnail_adm")
            setattr(field, "thumbnail_adm", ThumbnailField(size_filename))
            
            for size in self.sizes:
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
            Overwrite save_form_data to delete images and not to save
            if "delete" checkbox is selected
        '''
        if data is not None and data['deleted'] != '__deleted__':
            mode = getattr(BlocksImageField, data['mode'], None)
            if mode is not None:
                self.mode = mode
                setattr(instance, self.name + '___mode', mode)
            super(BlocksImageField, self).save_form_data(instance, data['file'])
        elif data is None:
            self.mode = None
            setattr(instance, self.name + '___mode', None)
        #else:
        #    print "delete images"


    def get_db_prep_save(self, value):
        '''
            Overwrite get_db_prep_save to allow saving nothing to the database
            if image has been deleted
        '''
        v = u''
        if value:
            v = super(BlocksImageField, self).get_db_prep_save(value)
        return v

    def contribute_to_class(self, cls, name):
        '''
        Call methods for generating all operations on specified signals
        '''
        super(BlocksImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._create_sizes, sender=cls)
        signals.post_init.connect(self._init_sizes,   sender=cls)
        signals.post_delete.connect(self._delete_sizes, sender=cls)


class GeoLocationField(Field):
    def get_internal_type(self):
        return "CharField"
    
    def formfield(self, **kwargs):
        kwargs['widget'] = GeoLocationWidget
        kwargs['form_class'] = GeoLocationFormField
        return super(GeoLocationField, self).formfield(**kwargs)

    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)
    
#class HTMLField(TextField):
#    def formfield(self, **kwargs):
#        kwargs['widget'] = widgets.HTMLWidget
#        return super(HTMLField, self).formfield(**defaults)
