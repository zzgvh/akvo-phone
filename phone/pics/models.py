# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.fields import ImageWithThumbnailsField

def image_path(instance, file_name, path_template='photo/%(instance_pk)s/%(file_name)s'):
    """
    Use to set ImageField upload_to attribute.
    Create path for image storing. When a new object instance is created we save
    in MEDIA_ROOT/db/project/temp/img_name.ext first and then immediately call
    save on the ImageFieldFile when the object instance has been saved to the db,
    so the path changes to MEDIA_ROOT/db/project/org.pk/img_name.ext.
    Modify path by supplying a path_tempate string
    """
    if instance.pk:
        instance_pk = str(instance.pk)
    else:
        # for new objects that have no id yet
        instance_pk = 'temp'
    return path_template % locals()

def tagbit_to_float(bit):
    bit = str(bit)
    bit = bit.split('/')
    if len(bit) == 2: #fraction
        return float(bit[0])/float(bit[1])
    else:
        return float(bit[0])

def exif_coord_to_decimal(pos_tag, ref_tag):
    '''
    takes an exif GPS GPSLatitude or GPS GPSLongitude tag and converts into a decimal coordinate
    '''
    pos_tag = pos_tag.values
    degrees = tagbit_to_float(pos_tag[0])
    minutes = tagbit_to_float(pos_tag[1])
    seconds = tagbit_to_float(pos_tag[2])
    decimal = degrees + minutes/60.0 + seconds/3600.0
    return decimal * (1 if ref_tag in ('N', 'E') else -1)
    
from PIL import Image
from PIL.ExifTags import TAGS


def get_lat_long(ret):
    Nsec = ret['GPSInfo'][2][2][0] / float(ret['GPSInfo'][2][2][1])
    Nmin = ret['GPSInfo'][2][1][0] / float(ret['GPSInfo'][2][1][1])
    Ndeg = ret['GPSInfo'][2][0][0] / float(ret['GPSInfo'][2][0][1])
    Wsec = ret['GPSInfo'][4][2][0] / float(ret['GPSInfo'][4][2][1])
    Wmin = ret['GPSInfo'][4][1][0] / float(ret['GPSInfo'][4][1][1])
    Wdeg = ret['GPSInfo'][4][0][0] / float(ret['GPSInfo'][4][0][1])

    if ret['GPSInfo'][1] == 'N':
        Nmult = 1
    else:
        Nmult = -1

    if ret['GPSInfo'][1] == 'E':
        Wmult = 1
    else:
        Wmult = -1

    Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
    Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
    return Lat,Lng

class Photo(models.Model):
    def creat_image_path(instance, file_name):
        "Create a path like 'db/project/<update.project.id>/update/<update.id>/image_name.ext'"
        path = 'pile/user/%d/%%(instance_pk)s/%%(file_name)s' % instance.user.pk
        return image_path(instance, file_name, path)
        
    user    = models.ForeignKey(User, related_name='photos',)
    photo   = ImageWithThumbnailsField(
                _('uploaded image'),
                upload_to=creat_image_path,
                thumbnail={'size': (240, 180), 'options': ('autocrop', 'detail', )}, #detail is a mild sharpen
                #help_text=_(''),
            )
    text = models.CharField(max_length=512, blank=True)
    upload_time = models.DateTimeField()
    
    def position(self):
        try:
            tags = {}
            i = Image.open(self.photo.file)
            info = i._getexif()    
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                tags[decoded] = value
            return get_lat_long(tags), tags['DateTimeOriginal']
        except:
            return 0.0, 0.0

    def original_time(self):
        try:
            tags = {}
            i = Image.open(self.photo.file)
            info = i._getexif()    
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                tags[decoded] = value
            return tags['DateTimeOriginal']
        except:
            return None