from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

from pure_pagination.mixins import PaginationMixin


from .models import CameraLens,CAMERA_LENS_BRANDS

class CameraLensDetailView(DetailView):

    model = CameraLens
    slug_field = 'slug'


class CameraLensListView(PaginationMixin, ListView):

    model = CameraLens
    paginate_by = 10


def list_brands(request):
    context = RequestContext(request)
    brands = CAMERA_LENS_BRANDS
    context_dict = {'brands': brands}
    """
        context_dict = {}
        for brand in brands:
            context_dict[str(brand[1])]
    """
    return render_to_response('camera_lens/cameralens_list_brands.html', context_dict, context)



"""
    def list_my_studio_classes(request, studioslug):
    context = RequestContext(request)
    studio = ZenStudio.objects.get(slug=studioslug)
    my_studio_class_list = ZenClass.objects.filter(zenstudio=studio)
    context_dict = {'my_studio_class_list': my_studio_class_list, 'studio': studio}
    return render_to_response('my_studio_class_list.html', context_dict, context)
"""
"""
professions_dict = {}
for i in range(len(names)):
    professions_dict[names[i]] = professions[i]
"""
