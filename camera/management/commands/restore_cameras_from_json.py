from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.core.management.base import BaseCommand, CommandError

from camera.models import Camera

class Command(BaseCommand):
    args = []
    help = 'backup Cameras to a json file'

    def handle(self, *args, **options):
        from django.core import serializers

        filename = "cameras.json"
        print("Restoring from " + filename)
        f = open( filename, 'r')
        data = f.read()

        for cam in serializers.deserialize("json", data):
            title = cam.object.title

            #print(title)

            try:
                c = Camera.objects.get(title=title)
            except Camera.DoesNotExist:
                c = None

            if c:
                print(c.title + " already exists in db...")
                #pass
            else:
                print("Doesnt exist, lets save to db.")
                cam.save()
