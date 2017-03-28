from __future__ import unicode_literals

import requests
from bs4 import BeautifulSoup

from django.utils.safestring import SafeUnicode
from django.core.management.base import BaseCommand, CommandError
from camera.models import Camera


CAMERA_BRANDS = ["Canon","Fujifilm","Leica","Nikon","Olympus","Panasonic","Pentax","Samsung","Sony"]

CANON_BRAND_SERIES_LIST = ["EOS", "EOS Rebel"]
FUJI_BRAND_SERIES_LIST = ["X series"]
LEICA_BRAND_SERIES_LIST = ["M series", "T series", ]
NIKON_BRAND_SERIES_LIST = ["CX (Nikon 1)", "DX", "FX"]
OLYMPUS_BRAND_SERIES_LIST = ["E series", "O-MD", "PEN"]
PANASONIC_BRAND_SERIES_LIST = ["Lumix G"]
PENTAX_BRAND_SERIES_LIST = ["K series", "Q series"]
SAMSUNG_BRAND_SERIES_LIST = ["NX"]
SONY_BRAND_SERIES_LIST = ["A-mount", "E-mount", "FE-mount"]

CANON_EOS_CAMERAS = ["10D","1D","1D C","1D Mark II","1D Mark II N","1D Mark III","1D Mark IV","1D X","1Ds","1Ds Mark II","1Ds Mark III","20D","20Da","300D","30D","40D","50D","5D","5D Mark II","5D Mark III","60D","60Da","6D","70D","7D","7D Mark II","D30","D60","M"]
CANON_EOS_REBEL_CAMERAS = ["SL1","T1i","T2i","T3","T3i","T4i","T5","T5i","XS","XSi","XT","XTi"]

FUJI_X_SERIES_CAMERAS = ["X-A1","X-E1","X-E2","X-M1","X-Pro1","X-T1"]

LEICA_M_SERIES_CAMERAS = ["M Typ 240","M-E Typ 220","M-Monochrom","M8","M8.2","M9","M9-P"]
LEICA_T_SERIES_CAMERAS = ["T (Typ 701)"]

NIKON_CX_CAMERAS = ["AW1","J1","J2","J3","J4","S1","S2","V1","V2","V3"]
NIKON_DX_CAMERAS = ["D100","D1H","D1X","D200","D2H","D2Hs","D2X","D2Xs","D300","D3000","D300S","D3100","D3200","D3300","D40","D40X","D50","D5000","D5100","D5200","D5300","D60","D70","D7000","D70s","D7100","D80","D90"]
NIKON_FX_CAMERAS = ["D3", "D3S", "D3X", "D4", "D4s", "D600", "D610", "D700", "D750", "D800", "D800E", "D810", "Df"]

OLYMPUS_E_SERIES_CAMERAS = ["E-1","E-3","E-30","E-300","E-330","E-410","E-420","E-450","E-5","E-500","E-510","E-520","E-600","E-620"]
OLYMPUS_OMD_CAMERAS = ["E-M1","E-M10","E-M5"]
OLYMPUS_PEN_CAMERAS = ["E-P1","E-P2","E-P3","E-P5","E-PL1","E-PL1s","E-PL2","E-PL3","E-PL5","E-PL6","E-PL7","E-PM1","E-PM2"]

PANASONIC_LUMIX_G_CAMERAS = ["G1","G10","G2","G3","G5","G6","GF1","GF2","GF3","GF5","GF6","GH1","GH2","GH3","GH4","GM1","GM5","GX1","GX7"]

PENTAX_K_SERIES_CAMERAS = ["K-01","K-3","K-30","K-5","K-5 II","K-5 IIs","K-50","K-500","K-7","K-m","K-r","K-S1","K-x","K100D","K100D Super","K10D","K110D","K200D","K20D"]
PENTAX_Q_SERIES_CAMERAS = ["Q","Q-S1","Q10","Q7"]

SAMSUNG_NX_CAMERAS = ["NX mini","NX1","NX10","NX100","NX1000","NX1100","NX20","NX200","NX2000","NX210","NX30","NX300","NX3000","NX300M"]

SONY_A_MOUNT_CAMERAS = ["Alpha DSLR-A100","Alpha DSLR-A200","Alpha DSLR-A230","Alpha DSLR-A290","Alpha DSLR-A300","Alpha DSLR-A330","Alpha DSLR-A350","Alpha DSLR-A390","Alpha DSLR-A500","Alpha DSLR-A550","Alpha DSLR-A560","Alpha DSLR-A580","Alpha DSLR-A700","Alpha DSLR-A850","Alpha DSLR-A900","Alpha SLT-A33","Alpha SLT-A35","Alpha SLT-A37","Alpha SLT-A55","Alpha SLT-A57","Alpha SLT-A58","Alpha SLT-A65","Alpha SLT-A77","Alpha SLT-A77 II","Alpha SLT-A99"]
SONY_E_MOUNT_CAMERAS = ["3","3N","5","5N","5R","5T","6","7","Alpha 3000","Alpha 5000","Alpha 5100","Alpha 6000","C3","F3"]
SONY_FE_MOUNT_CAMERAS = ["Alpha 7","Alpha 7 II","Alpha 7R","Alpha 7S"]

class Command(BaseCommand):

    help = "Populates SLR Cameras available on Amazon, and sets the title to the title from the flickr api."

    def handle(self, **options):
        for brand in CAMERA_BRANDS:
            if brand == 'Canon':
                for brand_series in CANON_BRAND_SERIES_LIST:
                    if brand_series == 'EOS':
                        for model in CANON_EOS_CAMERAS:
                            title = SafeUnicode(brand + " " + brand_series + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)

                    elif brand_series == 'EOS Rebel':
                        for model in CANON_EOS_REBEL_CAMERAS:
                            title = SafeUnicode(brand + " " + brand_series + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)

            elif brand == 'Fujifilm':
                for model in FUJI_X_SERIES_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series='X-Series', brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

            elif brand == 'Leica':
                for model in LEICA_M_SERIES_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series='M-Series', brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

                for model in LEICA_T_SERIES_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series='T-Series', brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

            elif brand == 'Nikon':
                for brand_series in NIKON_BRAND_SERIES_LIST:
                    if brand_series == 'CX (Nikon 1)':
                        for model in NIKON_CX_CAMERAS:
                            title = SafeUnicode(brand + " 1 " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)
                    elif brand_series == 'DX':
                        for model in NIKON_DX_CAMERAS:
                            title = SafeUnicode(brand + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)
                    elif brand_series == 'FX':
                        for model in NIKON_FX_CAMERAS:
                            title = SafeUnicode(brand + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)
            elif brand == 'Olympus':
                for brand_series in OLYMPUS_BRAND_SERIES_LIST:
                    if brand_series == 'E series':
                        for model in OLYMPUS_E_SERIES_CAMERAS:
                            title = SafeUnicode(brand + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)
                    elif brand_series == 'O-MD':
                        for model in OLYMPUS_OMD_CAMERAS:
                            title = SafeUnicode(brand + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)
                    elif brand_series == 'PEN':
                        for model in OLYMPUS_PEN_CAMERAS:
                            title = SafeUnicode(brand + " " + model)
                            try:
                                c = Camera.objects.get(title=title)
                                print("Was able to find " + c.title)
                            except:
                                print(title + " not found... creating.")
                                try:
                                    c = Camera.objects.create(title=title, brand=brand, series=brand_series, brand_model=model)
                                    print("Created " + c.title)
                                except:
                                    print("Something went wrong creating " + title)
            elif brand == 'Panasonic':
                for model in PANASONIC_LUMIX_G_CAMERAS:
                    title = SafeUnicode(brand + " DMC-" + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="Lumix G", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

            elif brand == 'Pentax':
                for model in PENTAX_K_SERIES_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="K-Series", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

                for model in PENTAX_Q_SERIES_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="Q-Series", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)
            elif brand == 'Samsung':
                for model in SAMSUNG_NX_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="NX", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)
            elif brand == 'Sony':
                for model in SONY_A_MOUNT_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="A-Mount", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

                for model in SONY_E_MOUNT_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="E-Mount", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)

                for model in SONY_FE_MOUNT_CAMERAS:
                    title = SafeUnicode(brand + " " + model)
                    try:
                        c = Camera.objects.get(title=title)
                        print("Was able to find " + c.title)
                    except:
                        print(title + " not found... creating.")
                        try:
                            c = Camera.objects.create(title=title, brand=brand, series="FE-Mount", brand_model=model)
                            print("Created " + c.title)
                        except:
                            print("Something went wrong creating " + title)
            else:
                print("should never get here")



        """
            Lets get the flickr data for all this now...
        """

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
