from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django_extensions.db.models import TimeStampedModel,TitleSlugDescriptionModel
from django.core.urlresolvers import reverse

from camera_lens.models import CameraLens


@python_2_unicode_compatible
class Camera(TimeStampedModel,TitleSlugDescriptionModel):
    brand = models.CharField(max_length=200, blank=True)
    series = models.CharField(max_length=32, blank=True)    # DX vs FX, EOS, EOS Rebel, etc.
    brand_model = models.CharField(max_length=32, blank=True)
    lenses = models.ManyToManyField(CameraLens, blank=True)

    megapixels = models.FloatField(null=True, blank=True)
    lcd_screen_size = models.CharField(max_length=8, blank=True)
    memory_type = models.CharField(max_length=200, blank=True)

    product_thumb_sm = models.URLField(blank=True)
    product_thumb_sm_url = models.URLField(blank=True)
    product_thumb_lg = models.URLField(blank=True)
    product_thumb_lg_url = models.URLField(blank=True)

    amazon_asin = models.CharField(max_length=24, blank=True)
    amazon_detail_page_url = models.URLField(max_length=512, blank=True)
    amazon_review_page_url = models.URLField(max_length=512, blank=True)
    amazon_review_iframe_url = models.CharField(max_length=1024, blank=True)

    amazon_image_thumb_sm = models.URLField(blank=True)
    amazon_image_thumb_lg = models.URLField(blank=True)
    amazon_image_sm = models.URLField(blank=True)
    amazon_image_md = models.URLField(blank=True)
    amazon_image_lg = models.URLField(blank=True)

    flickr_title = models.CharField(max_length=255, blank=True)
    flickr_id = models.CharField(max_length=64, blank=True)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        slug = self.slug
        return reverse("camera-detail", kwargs={"slug": slug})
