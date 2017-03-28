from django.core.management.base import BaseCommand, CommandError
from camera_lens.models import CameraLens


class Command(BaseCommand):


    def handle(self, **options):
        lenses = CameraLens.objects.all()
        for lens in lenses:
            print(lens.title)
