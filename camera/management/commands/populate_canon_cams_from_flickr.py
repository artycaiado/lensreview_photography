from django.core.management.base import BaseCommand, CommandError
from camera.models import CameraBrand, Camera

import requests
from bs4 import BeautifulSoup


FLICKR_API_KEY = "5bed1c943aa807537d79a3656dc0dfc8"
FLICKR_ENDPOINT = "https://api.flickr.com/services"
FLICKR_CAMERA_BRAND = "canon"
FLICKR_CAMERA_GETBRANDMODELS_URI = "/rest/?method=flickr.cameras.getBrandModels&api_key=" + FLICKR_API_KEY + "&brand=" + FLICKR_CAMERA_BRAND


REQUEST_URL = FLICKR_ENDPOINT + FLICKR_CAMERA_GETBRANDMODELS_URI

class Command(BaseCommand):


    def handle(self, **options):


        r = requests.get(REQUEST_URL)
        data = r.text
        soup = BeautifulSoup(data)

        for cam in soup.findAll("camera"):
            cam_title = cam.find("name").text
            try:
                cam_megapixels = cam.find("megapixels").text
            except:
                cam_megapixels = "Unknown"

            try:
                cam_lcd_screen_size = cam.find("lcd_screen_size").text
            except:
                cam_lcd_screen_size = "Unknown"

            try:
                cam_memory_type = cam.find("memory_type").text
            except:
                cam_memory_type = "Unknown"

            try:
                cam_sm_thumb = cam.find("small").text
            except:
                cam_sm_thumb = "Unavailable"

            try:
                cam_lg_thumb = cam.find("large").text
            except:
                cam_lg_thumb = "Unavailable"

            c, created = Camera.objects.get_or_create(title=cam_title, brand=CameraBrand.objects.get(title="Canon"), megapixels=cam_megapixels, lcd_screen_size=cam_lcd_screen_size, memory_type=cam_memory_type, product_thumb_sm=cam_sm_thumb, product_thumb_lg=cam_lg_thumb)
            if created:
                print("Created " + cam_title)
            else:
                print(cam_title + " already existed in the database.")
