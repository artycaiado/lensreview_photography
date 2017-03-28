from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.core.management.base import BaseCommand, CommandError

from camera.models import Camera

class Command(BaseCommand):
    args = []
    help = 'backup cameras to a json file'

    def handle(self, *args, **options):
        from django.core import serializers
        data = serializers.serialize("json", Camera.objects.all())

        #print(data)
        filename = "cameras.json"
        print("Backing up to " + filename)
        f = open( filename, 'w')
        f.write(data)
