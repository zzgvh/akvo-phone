# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext, loader
from django.views.decorators.csrf import csrf_response_exempt
from django.utils.translation import ugettext_lazy as _, get_language

from models import Photo

from datetime import datetime

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    From: http://www.djangosnippets.org/snippets/821/
    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                # add current language for template caching purposes
                output[0].update({'lang':get_language()})
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                # add current language for template caching purposes
                output.update({'lang':get_language()})
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

class GeoUpdateForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('photo', 'text', 'hdop', )

class HttpResponseNoContent(HttpResponse):
    status_code = 204    

@csrf_response_exempt
def upload_photo(request, user_id=1):
    if request.method == 'POST':
#        user = get_object_or_404(User, pk=request.POST.getitem('user', 1))
        user = get_object_or_404(User, pk=user_id)

        form = GeoUpdateForm(request.POST, request.FILES, )
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.upload_time = datetime.now()
            new_photo.user = user
            new_photo.save()
            return HttpResponse(str(new_photo.id))
        return HttpResponseForbidden()
    return HttpResponseBadRequest()

@render_to('pics/templates/index.html')
def photos(request):
    photos = Photo.objects.all()
    return {
        'photos': photos,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

