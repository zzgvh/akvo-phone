# -*- coding: utf-8 -*-

#to be run in the akvo rsr root folder. setting up all projects as published, if they have no status
# and setting all orgs to free account if they have none

from django.core.management import setup_environ
from django.core.paginator import Paginator
    
import settings
setup_environ(settings)

from django.contrib.auth.models import Group, User

from os.path import basename, splitext

from pics.models import *
from django.db.models.fields.files import ImageField

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

def main():
    p = Photo.objects.get(pk=1)
    print p.position()

#    tags = {}
#    i = Image.open(p.photo.file)
#    print i
#    info = i._getexif()    
#    for tag, value in info.items():
#        decoded = TAGS.get(tag, tag)
#        print decoded
#        tags[decoded] = value
#    print get_lat_long(tags)
        
#    lat  = tags['GPS GPSLatitude']
#    ns = str(tags['GPS GPSLatitudeRef'])
#    goog_lat = exif_coord_to_decimal(lat, ns)
#    long = tags['GPS GPSLongitude']
#    ew = str(tags['GPS GPSLongitudeRef'])
#    goog_long = exif_coord_to_decimal(long, ew)
#    print goog_lat, goog_long
    
if __name__ == '__main__':
    main()
