# -*- coding: utf-8 -*-

#from django import forms
#from django.conf import settings
from django.contrib import admin
from django.db.models import get_model

from sorl.thumbnail.fields import ImageWithThumbnailsField

class PhotoAdmin(admin.ModelAdmin):
#    fieldsets = (
#        (_(u'General information'), {'fields': ('name', 'long_name', 'organisation_type', 'logo', 'city', 'state', 'country', 'url', 'map', )}),
#        (_(u'Contact information'), {'fields': ('address_1', 'address_2', 'postcode', 'phone', 'mobile', 'fax',  'contact_person',  'contact_email',  ), }),
#        (_(u'About the organisation'), {'fields': ('description', )}),
#    )    
#    list_display = ('name', 'long_name', 'website', 'partner_types', )

    #Methods overridden from ModelAdmin (django/contrib/admin/options.py)
    def __init__(self, model, admin_site):
        """
        Override to add self.formfield_overrides.
        Needed to get the ImageWithThumbnailsField working in the admin.
        """
        self.formfield_overrides = {ImageWithThumbnailsField: {'widget': admin.widgets.AdminFileWidget},}
        super(PhotoAdmin, self).__init__(model, admin_site)

admin.site.register(get_model('pics', 'photo'), PhotoAdmin)