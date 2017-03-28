from __future__ import unicode_literals

import requests
import time
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

from camera.models import Camera, CameraBrand

FLICKR_API_KEY = "5bed1c943aa807537d79a3656dc0dfc8"
FLICKR_ENDPOINT = "https://api.flickr.com/services"


def get_brands_from_flickr():
    FLICKR_CAMERA_GETBRANDS_URI = "/rest/?method=flickr.cameras.getBrands&api_key=" + FLICKR_API_KEY
    REQUEST_URL = FLICKR_ENDPOINT + FLICKR_CAMERA_GETBRANDS_URI
    try:
        r = requests.get(REQUEST_URL)
        data = r.text
        soup = BeautifulSoup(data)
        brands = soup.findAll("brand")
        return brands
    except:
        print("error fetching brands from flickr...")


def create_camera_brand_in_django_db(b, bid):
    camera_brand, created = CameraBrand.objects.get_or_create(title=b, flickr_id=bid)
    if created:
        print("Created brand: " + b)
    else:
        print(b + " is already in the database")


def create_cameras_per_brand_from_flickr(bid):
    FLICKR_CAMERA_BRAND_ID = bid
    FLICKR_CAMERA_GETBRANDMODELS_URI = "/rest/?method=flickr.cameras.getBrandModels&api_key=" + FLICKR_API_KEY + "&brand=" + FLICKR_CAMERA_BRAND_ID
    REQUEST_URL = FLICKR_ENDPOINT + FLICKR_CAMERA_GETBRANDMODELS_URI
    try:
        r = requests.get(REQUEST_URL)
        data = r.text
        soup = BeautifulSoup(data)
    except:
        print("error looking up " + bid + " cameras on flickr...")

    for cam in soup.findAll("camera"):
        # investigate
        # from django.utils.safestring import SafeUnicode
        # cam_title=SafeUnicode(cam.find("name").text)
        cam_title_soup = unicode(cam.find("name").text)
        cam_title_soup2 = cam_title_soup.replace(u"\u2122", '')
        cam_title = cam_title_soup2.replace(u"\u03bc", '')

        try:
            cam_id = cam['id']
        except:
            cam_id = "Unknown"
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

        # fix this and only try on title and then do the defaults thing like in
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/ to avoid duplicates
        c, created = Camera.objects.get_or_create(title=cam_title, brand=CameraBrand.objects.get(flickr_id=bid), megapixels=cam_megapixels, lcd_screen_size=cam_lcd_screen_size, memory_type=cam_memory_type, product_thumb_sm=cam_sm_thumb, product_thumb_lg=cam_lg_thumb, flickr_id=cam_id)
        if created:
            print("Created " + cam_title)
        else:
            print(cam_title + " already existed in the database.")


class Command(BaseCommand):
    def handle(self, **options):

        print("Populating camera brands first...")
        brands = get_brands_from_flickr()
        for brand in brands:
            b = (brand['name'])
            bid = (brand['id'])
            create_camera_brand_in_django_db(b=b, bid=bid)
            create_cameras_per_brand_from_flickr(bid=bid)
            time.sleep(1)

        print("Finished populating cameras and camera brands...")
