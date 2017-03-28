from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from camera.models import Camera


class Command(BaseCommand):


    def handle(self, **options):
        cams = Camera.objects.all()
        for cam in cams:
            print(cam)
