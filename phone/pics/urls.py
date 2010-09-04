# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    url(r'upload/$', 'pics.views.upload_photo', name='views_upload_photo'),
    url(r'$', 'pics.views.photos', name='views_photos'),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
