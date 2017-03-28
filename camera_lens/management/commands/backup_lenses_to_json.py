from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.core.management.base import BaseCommand, CommandError

from camera_lens.models import CameraLens

class Command(BaseCommand):
    args = []
    help = 'backup CameraLenses to a json file'

    def handle(self, *args, **options):
        from django.core import serializers
        data = serializers.serialize("json", CameraLens.objects.all())

        #print(data)
        filename = "camera_lenses.json"
        print("Backing up to " + filename)
        f = open( filename, 'w')
        f.write(data)


"""
# look at this for backing up cam + lenses together lensreview_photography.management.commands maybe?
all_objects = list(Restaurant.objects.all()) + list(Place.objects.all())
data = serializers.serialize('xml', all_objects)
"""
