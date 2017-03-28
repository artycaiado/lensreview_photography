from __future__ import unicode_literals

import datetime
from haystack import indexes
from .models import Camera


class CameraIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    brand = indexes.CharField(model_attr='brand', faceted=True, null=True)
    megapixels = indexes.FloatField(model_attr='megapixels', faceted=True, null=True)
    title = indexes.EdgeNgramField(model_attr='title', null=True)

    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Camera

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
