from __future__ import unicode_literals
from django.utils.safestring import SafeUnicode

import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from camera.models import Camera



BRANDS = ["canon", "nikon", "fujifilm", "leica", "olympus", "panasonic", "pentax", "samsung", "sony"]

class Command(BaseCommand):
    def handle(self, **options):

        print("If you have time, put this in a nice for loop, should be simple but this works and got the data, plenty of other stuff to focus on...")

        for b in BRANDS:
            print(b)

        canon_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=canon"
        canon_resp = requests.get(canon_url)
        canon_soup = BeautifulSoup(canon_resp.text)
        canon_cameras = canon_soup.findAll("camera")

        for c in canon_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")
            try:
                cam = Camera.objects.get(flickr_title=title)
            except:
                pass

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()


        nikon_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=nikon"
        nikon_resp = requests.get(nikon_url)
        nikon_soup = BeautifulSoup(nikon_resp.text)
        nikon_cameras = nikon_soup.findAll("camera")
        for c in nikon_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()


        fuji_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=fujifilm"
        fuji_resp = requests.get(fuji_url)
        fuji_soup = BeautifulSoup(fuji_resp.text)
        fuji_cameras = fuji_soup.findAll("camera")
        for c in fuji_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()


        leica_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=leica"
        leica_resp = requests.get(leica_url)
        leica_soup = BeautifulSoup(leica_resp.text)
        leica_cameras = leica_soup.findAll("camera")
        for c in leica_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()

        olympus_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=olympus"
        olympus_resp = requests.get(olympus_url)
        olympus_soup = BeautifulSoup(olympus_resp.text)
        olympus_cameras = olympus_soup.findAll("camera")
        for c in olympus_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()

        panasonic_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=panasonic"
        panasonic_resp = requests.get(panasonic_url)
        panasonic_soup = BeautifulSoup(panasonic_resp.text)
        panasonic_cameras = panasonic_soup.findAll("camera")
        for c in panasonic_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()

        pentax_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=pentax"
        pentax_resp = requests.get(pentax_url)
        pentax_soup = BeautifulSoup(pentax_resp.text)
        pentax_cameras = pentax_soup.findAll("camera")
        for c in pentax_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()

        samsung_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=samsung"
        samsung_resp = requests.get(samsung_url)
        samsung_soup = BeautifulSoup(samsung_resp.text)
        samsung_cameras = samsung_soup.findAll("camera")
        for c in samsung_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()


        # sony might not match on anything but we can try anyway...
        sony_url = "https://api.flickr.com/services/rest/?method=flickr.cameras.getBrandModels&api_key=5bed1c943aa807537d79a3656dc0dfc8&brand=sony"
        sony_resp = requests.get(sony_url)
        sony_soup = BeautifulSoup(sony_resp.text)
        sony_cameras = sony_soup.findAll("camera")
        for c in sony_cameras:
            cam = None
            title = SafeUnicode(c.find("name").text)
            try:
                cam = Camera.objects.get(title=title)
            except:
                pass
                #print(title + " does not exist in db... skipping")

            if cam:
                print("Populating data from flickr for " + cam.title)
                cam.flickr_title = title
                if not cam.flickr_id:
                    try:
                        cam.flickr_id = SafeUnicode(c['id'])
                    except:
                        pass
                if not cam.megapixels:
                    try:
                        cam.megapixels = SafeUnicode(c.find("megapixels").text)
                    except:
                        pass
                if not cam.lcd_screen_size:
                    try:
                        cam.lcd_screen_size = SafeUnicode(c.find("lcd_screen_size").text)
                    except:
                        pass
                if not cam.memory_type:
                    try:
                        cam.memory_type = SafeUnicode(c.find("memory_type").text)
                    except:
                        pass
                if not cam.product_thumb_sm_url:
                    try:
                        cam.product_thumb_sm_url = SafeUnicode(c.find("small").text)
                    except:
                        pass
                if not cam.product_thumb_lg_url:
                    try:
                        cam.product_thumb_lg_url = SafeUnicode(c.find("large").text)
                    except:
                        pass
                cam.save()
