from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

# sitemap related stuff
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap
from camera.models import Camera
from camera_lens.models import CameraLens

cameras_dict = {
    'queryset': Camera.objects.all(),
}

cameralenses_dict = {
    'queryset': CameraLens.objects.all(),
}

sitemaps = {
    'cameras': GenericSitemap(cameras_dict, priority=.6),
    'camera_lenses': GenericSitemap(cameralenses_dict, priority=.6),
}

"""
# taken from https://docs.djangoproject.com/en/1.7/ref/contrib/sitemaps/#django.contrib.sitemaps.GenericSitemap

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'blog': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns = patterns('',
    # some generic view using info_dict
    # ...

    # the sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
)

"""

urlpatterns = patterns('',
    url(r'^$', include('haystack.urls')),
    url(r'^cameras/', include('camera.urls')),
    url(r'^lenses/', include('camera_lens.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^review/', include('review.urls')),

    url(r'^search/', include('haystack.urls')),
    url(r'^search/autocomplete/', 'camera.views.autocomplete'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


"""
# Haystack Facet notes:
from django.conf.urls.defaults import *
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


sqs = SearchQuerySet().facet('author')


urlpatterns = patterns('haystack.views',
    url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
)




# Teamplate
{% if query %}
    <!-- Begin faceting. -->
    <h2>By Author</h2>

    <div>
        <dl>
            {% if facets.fields.author %}
                <dt>Author</dt>
                {# Provide only the top 5 authors #}
                {% for author in facets.fields.author|slice:":5" %}
                    <dd><a href="{{ request.get_full_path }}&amp;selected_facets=author_exact:{{ author.0|urlencode }}">{{ author.0 }}</a> ({{ author.1 }})</dd>
                {% endfor %}
            {% else %}
                <p>No author facets.</p>
            {% endif %}
        </dl>
    </div>
    <!-- End faceting -->

    <!-- Display results... -->
    {% for result in page.object_list %}
        <div class="search_result">
 

"""
