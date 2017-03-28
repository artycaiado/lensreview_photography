from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.core.management.base import BaseCommand, CommandError

from camera_lens.models import CameraLens

class Command(BaseCommand):
    args = []
    help = 'backup CameraLenses to a json file'

    def handle(self, *args, **options):
        from django.core import serializers

        filename = "camera_lenses.json"
        print("Restoring from " + filename)
        f = open( filename, 'r')
        data = f.read()

        for lens in serializers.deserialize("json", data):
            title = lens.object.title
            amazon_asin = lens.object.amazon_asin
            if lens.object.lens_zoom:
                lens.object.lens_zoom = lens.object.lens_zoom[:10]

            #print(title + " " + amazon_asin)

            try:
                l = CameraLens.objects.get(title=title, amazon_asin=amazon_asin)
            except CameraLens.DoesNotExist:
                l = None

            if l:
                print(l.title + " already exists in db...")
                #pass
            else:
                print("Doesnt exist, lets save to db.")
                lens.save()



"""
# look at this for backing up cam + lenses together lensreview_photography.management.commands maybe?
all_objects = list(Restaurant.objects.all()) + list(Place.objects.all())
data = serializers.serialize('xml', all_objects)
"""
