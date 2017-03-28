from __future__ import unicode_literals

import datetime
from haystack import indexes
from .models import CameraLens


class CameraLensIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title', null=True)
    lens_brand = indexes.CharField(model_attr='lens_brand', faceted=True)
    aperture_wide_max = indexes.CharField(model_attr='aperture_wide_max', faceted=True, null=True)
    lens_sensor = indexes.CharField(model_attr='lens_sensor', faceted=True, null=True)
    focus_motor = indexes.CharField(model_attr='focus_motor', faceted=True, null=True)
    focus_technology = indexes.CharField(model_attr='focus_technology', faceted=True, null=True)
    focal_length_max = indexes.CharField(model_attr='focal_length_max', faceted=True, null=True)
    focal_length_min = indexes.CharField(model_attr='focal_length_min', faceted=True, null=True)


    def prepare_lens_brand(self,obj):
        return obj.get_lens_brand_display()

    def get_model(self):
        return CameraLens


    def index_queryset(self, using=None):
        return self.get_model().objects.all()
