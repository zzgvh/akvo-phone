# -*- coding: utf-8 -*-

# Django imports
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Django app imports
from sorl.thumbnail.fields import ImageWithThumbnailsField

# Python libraries iports
from PIL import Image
from PIL.ExifTags import TAGS


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



def get_lat_long(ret):
    try:
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
    except:
        return 0.0, 0.0

def exif_tags(fname):
    """
    populate tags with all EXIF data from an image
    fname is the full path file name if the image
    """
    try:
        tags = {}
        image = Image.open(fname)
        info = image._getexif()    
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            tags[decoded] = value
        return tags
    except:
        return {}

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
        return get_lat_long(exif_tags(str(self.photo.file)))

    def original_time(self):
        tags = exif_tags(str(self.photo.file))
        return tags['DateTimeOriginal']
