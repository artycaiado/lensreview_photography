from __future__ import unicode_literals

from django.conf.urls import patterns, url

#from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from .forms import CameraLensFacetedSearchForm

from .models import CameraLens
from .views import CameraLensDetailView, CameraLensListView, list_brands

#sqs = SearchQuerySet().models(CameraLens).facet('lens_brand')
sqs = SearchQuerySet().models(CameraLens).facet('lens_brand').facet('aperture_wide_max').facet('lens_sensor').facet('focus_motor').facet('focus_technology').facet('focal_length_max').facet('focal_length_min')


urlpatterns = patterns('',
    url(r'^$', FacetedSearchView(template='camera_lens/cameralens_faceted_search.html', form_class=CameraLensFacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    #url(r'^$', CameraLensListView.as_view(), name='lens-list'),
    url(r'^browse/$', FacetedSearchView(template='camera_lens/cameralens_faceted_search.html', form_class=CameraLensFacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    url(r'^brands/$', list_brands),
    url(r'^(?P<slug>[-_\w]+)/$', CameraLensDetailView.as_view(), name='lens-detail'),

)
