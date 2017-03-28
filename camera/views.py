from __future__ import unicode_literals

import json

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin

from django.http import HttpResponse
from django.utils import timezone

from haystack.query import SearchQuerySet
#from haystack.views import FacetedSearchView

from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Camera
from .forms import CameraSearchForm

class CameraDetailView(DetailView):

    model = Camera
    slug_field = 'slug'


class CameraListView(PaginationMixin, FormMixin, ListView):

    model = Camera
    paginate_by = 10

    # not working at the moment
    #form_class = CameraSearchForm

    # this get_queryset is for EdgeNgram haystack searching
    def get_queryset(self):
        term = self.request.REQUEST.get('search')

        if term:
            return self.model.objects.filter(title__icontains=term)
        else:
            return self.model.objects.all()


"""
    def get(self, request, *args, **kwargs):
            # From ProcessFormMixin
            form_class = self.get_form_class()
            self.form = self.get_form(form_class)

            # From BaseListView
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()
            if not allow_empty and len(self.object_list) == 0:
                raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                              % {'class_name': self.__class__.__name__})

            context = self.get_context_data(object_list=self.object_list, form=self.form)
            return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
            return self.get(request, *args, **kwargs)
"""


def search_cameras(request):

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    context = RequestContext(request)

    if request.method == "POST":
        form = CameraSearchForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            cams = Camera.objects.filter(brand__icontains=brand).order_by('title')
            p = Paginator(cams, 100, request=request)
            cameras = p.page(page)
            context_dict = {'cameras': cameras, 'form': form, }
            return render_to_response("camera/camera_generic_search.html", context_dict, context)

    else:
        form = CameraSearchForm()
    return render_to_response("camera/camera_generic_search.html", {
        "form": form,
    }, context)

"""

def list_brands(request):
    context = RequestContext(request)
    brands = CameraBrand.objects.all()
    context_dict = {'brands': brands}
    return render_to_response('camera/camera_list_brands.html', context_dict, context)
"""

"""

# needed for ajax

def search_titles(request):
    cameras = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))

    return render_to_response('ajax_search.html', {'cameras' : cameras})


# with the ajax_search.html looking like this:

{% if cameras.count > 0 %}

    {% for camera in cameras %}
        <li><a href="{{camera.object.get_absolute_url}}">{{camera.object.title}}</a></li>
    {% endfor %}
{% else %}
    <li>Nothing to show!</li>
{% endif %}


"""

# this is the autocomplete for django haystack
def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
