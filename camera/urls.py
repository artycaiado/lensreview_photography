from __future__ import unicode_literals
from django.conf.urls import patterns, url
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from .models import Camera
from .views import CameraDetailView, CameraListView, search_cameras
from .forms import CameraFacetedSearchForm



#sqs = SearchQuerySet().models(Camera).load_all().facet('brand')
#sqs = SearchQuerySet().models(Camera).facet('brand').facet('megapixels').auto_query('')
sqs = SearchQuerySet().models(Camera).facet('brand').facet('megapixels').order_by('-megapixels', 'brand')
#sqs = SearchQuerySet().facet('brand')


urlpatterns = patterns('',
    url(r'^$', FacetedSearchView(template='camera/camera_faceted_search.html', form_class=CameraFacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    #url(r'^$', CameraListView.as_view(), name='camera-list'),
    #url(r'^brands/$', list_brands),
    url(r'^search/$', search_cameras),
    url(r'^browse/$', FacetedSearchView(template='camera/camera_faceted_search.html', form_class=CameraFacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    #url(r'^browse/$', FacetedSearchView(template='camera/camera_faceted_search.html', form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    #url(r'^brands/$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    url(r'^(?P<slug>[-_\w]+)/$', CameraDetailView.as_view(), name='camera-detail'),
)



"""
urlpatterns += patterns('haystack.views',
    url(r'^brands/$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=cambrand_sqs), name='haystack_search'),
)
"""
