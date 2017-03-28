from django.contrib import admin
from .models import Camera


class CameraAdmin(admin.ModelAdmin):

    list_display = ('title', 'brand', 'series', 'amazon_asin', 'flickr_title', 'megapixels', 'memory_type')

admin.site.register(Camera,CameraAdmin)
