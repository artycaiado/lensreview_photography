from __future__ import unicode_literals

from django.contrib import admin
from .models import CameraLens, CameraLensExamplePhoto, CameraLensProductPhoto


class CameraLensExamplePhotoInline(admin.TabularInline):
    model = CameraLensExamplePhoto
    extra = 3


class CameraLensProductPhotoInline(admin.TabularInline):
    model = CameraLensProductPhoto
    extra = 3


class CameraLensAdmin(admin.ModelAdmin):

    list_display = ('title', 'amazon_asin', 'lens_brand','aperture_wide_max', 'aperture_zoom_max', 'focal_length_min', 'focal_length_max', 'lens_sensor', 'image_stabilization', 'focus_motor', 'focus_technology' )
    #prepopulated_fields = {'slug': ('title',)}
    inlines = [CameraLensExamplePhotoInline, CameraLensProductPhotoInline, ]


admin.site.register(CameraLens, CameraLensAdmin)
