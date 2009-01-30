from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings

class DelAdminFileWidget(AdminFileWidget):
    '''
    A AdminFileWidget that shows a delete checkbox
    '''
    input_type = 'file'

    def render(self, name, value, attrs=None):
        input = super(forms.widgets.FileInput, self).render(name, value, attrs)
        if value:
            from blocks.forms import fields
            thumbnail = None
            #if isinstance(value, fields.BlocksImageField):
            try:
                thumbnail = getattr(value, 'thumbnail')
            except AttributeError:
                pass

            item = '<div><label>%s</label>%s</div>'
            output = []
            output.append('<div class="form-row">')
            if isinstance(value, fields.BlocksImageField) and thumbnail != None:
                output.append(item % (_('Currently:'), '<img src="%s%s" alt="%s"/>' % (settings.MEDIA_URL, thumbnail.name, value)))
            output.append(item % (_('Change:'), input))
            if isinstance(value, fields.BlocksImageField):
                output.append(item % (_('Delete') + ':', '<input type="checkbox" name="%s_delete"/>' % name)) # split colon to force "Delete" that is already translated
            output.append('</div>')
            return mark_safe(u''.join(output))
        else:
            return mark_safe(input)

    def value_from_datadict(self, data, files, name):
        if not data.get('%s_delete' % name):
            return super(DelAdminFileWidget, self).value_from_datadict(data, files, name)
        else:
            return '__deleted__'



DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 300

class GeoLocationWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)

        super(GeoLocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        from django.utils.safestring import mark_safe
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
        lat, lng = float(a), float(b)

        js = '''
<script type="text/javascript">
//<![CDATA[

    var map_%(name)s;

    function savePosition_%(name)s(point)
    {
	    var latitude = document.getElementById("id_%(name)s");
	    //var longitude = document.getElementById("id_%(name)s_longitude");
	    latitude.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
	    //longitude.value = point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }

    function load_%(name)s() {
        if (GBrowserIsCompatible()) {
            map_%(name)s = new GMap2(document.getElementById("map_%(name)s"));
            map_%(name)s.addControl(new GSmallMapControl());
            map_%(name)s.addControl(new GMapTypeControl());

            var point = new GLatLng(%(lat)f, %(lng)f);
            map_%(name)s.setCenter(point, 8);
            m = new GMarker(point, {draggable: true});

            GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    savePosition_%(name)s(point);
            });

            map_%(name)s.addOverlay(m);

            /* save coordinates on clicks */
            GEvent.addListener(map_%(name)s, "click", function (overlay, point) {
                savePosition_%(name)s(point);

                map_%(name)s.clearOverlays();
                m = new GMarker(point, {draggable: true});

                GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    savePosition_%(name)s(point);
                });

                map_%(name)s.addOverlay(m);
            });
        }
    }
//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat,lng), dict(id='id_%s' % name))
        html += "<div id=\"map_%s\" class=\"gmap\" style=\"width: %dpx; height: %dpx\"></div>" % (name, self.map_width, self.map_height)

        return mark_safe(js+html)

    class Media:
        js = ("http://maps.google.com/maps?file=api&v=2&key=%s" % settings.GOOGLE_MAPS_API_KEY, 'blocks/js/map.js')
