from django import forms
from django.utils.translation import ugettext_lazy as _

import floppyforms
from haystack.forms import SearchForm

from .models import CameraLens


class CameraLensFacetedSearchForm(SearchForm):
    #min_megapixels = forms.IntegerField(required=False)
    #max_megapixels = forms.IntegerField(required=False)
#    brand = forms.ModelChoiceField(queryset=CameraLens.objects.all().values_list('brand', flat=True).order_by().distinct(), to_field_name='brand', required=False)
#    min_megapixels = floppyforms.IntegerField(widget=MegaPixelSlider, required=False,)
#    max_megapixels = floppyforms.IntegerField(widget=MegaPixelSlider, required=False)
#    min_megapixels = floppyforms.IntegerField(widget=floppyforms.NumberInput, required=False, initial=7)
#    max_megapixels = floppyforms.IntegerField(widget=floppyforms.NumberInput, required=False, initial=50)
    """
    def clean_min_megapixels(self):
        min_megapixels = self.cleaned_data['min_megapixels']
        if not 1 <= min_megapixels <= 50:
            raise floppyforms.ValidationError("Enter a value between 1 and 50")

        if not min_megapixels % 1 == 0:
            raise floppyforms.ValidationError("Enter a multiple of 1")

        return min_megapixels

    def clean_max_megapixels(self):
        max_megapixels = self.cleaned_data['max_megapixels']
        if not 1 <= max_megapixels <= 50:
            raise floppyforms.ValidationError("Enter a value between 1 and 50")

        if not max_megapixels % 1 == 0:
            raise floppyforms.ValidationError("Enter a multiple of 1")

        return max_megapixels

    def clean_brand(self):
        brand = self.cleaned_data['brand']
        return brand
    """
    def no_query_found(self):
        return self.searchqueryset.all()

    def __init__(self, *args, **kwargs):
        self.selected_facets = kwargs.pop("selected_facets", [])
        super(CameraLensFacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(CameraLensFacetedSearchForm, self).search()
        """
        if self.is_valid() and self.cleaned_data['min_megapixels']:
            sqs = sqs.filter(megapixels__gte=self.cleaned_data['min_megapixels'])

        if self.is_valid() and self.cleaned_data['max_megapixels']:
            sqs = sqs.filter(megapixels__lte=self.cleaned_data['max_megapixels'])

        if self.is_valid() and self.cleaned_data['brand']:
            sqs = sqs.filter(brand__exact=self.cleaned_data['brand'])
        """
        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

            #if field == 'brand_exact':
            #    self.active_filter['selected_facets'] = ('brand', value)

        return sqs
