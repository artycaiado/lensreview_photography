import random
import re
import requests
import sys
import time

import bottlenose
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError

from camera.models import Camera
from camera_lens.models import CameraLens


AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
AWS_ASSOCIATE_TAG=''

amazon = bottlenose.Amazon(AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG)


# I don't know the URL to look these up, but these are what amazon has in the finder as of 1/08/2014
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


# set the headers to something other than python user agent.
r_headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0' }

def list_brand_series(brand):
    if brand == 'Canon':
        # can re-work this later incorporating url to get all the series but since its not updated often and the urls are tricky hard-coding per brand for now
        return CANON_BRAND_SERIES_LIST
    elif brand == 'Fujifilm':
        return FUJI_BRAND_SERIES_LIST
    elif brand == 'Leica':
        return LEICA_BRAND_SERIES_LIST
    elif brand == 'Nikon':
        return NIKON_BRAND_SERIES_LIST
    elif brand == 'Olympus':
        return OLYMPUS_BRAND_SERIES_LIST
    elif brand == 'Panasonic':
        return PANASONIC_BRAND_SERIES_LIST
    elif brand == 'Pentax':
        return PENTAX_BRAND_SERIES_LIST
    elif brand == 'Samsung':
        return SAMSUNG_BRAND_SERIES_LIST
    elif brand == "Sony":
        return SONY_BRAND_SERIES_LIST
    else:
        print("Sorry no matches for this, this should never happen, going to exit now with error.")
        sys.exit(1)


def list_brand_series_models(brand, brand_series):
    if brand == 'Canon':
        if brand_series == 'EOS':
            return CANON_EOS_CAMERAS
        elif brand_series == 'EOS Rebel':
            return CANON_EOS_REBEL_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Fujifilm':
        if brand_series == 'X series':
            return FUJI_X_SERIES_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Leica':
        if brand_series == 'M series':
            return LEICA_M_SERIES_CAMERAS
        elif brand_series == 'T series':
            return LEICA_T_SERIES_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Nikon':
        if brand_series == 'CX (Nikon 1)':
            return NIKON_CX_CAMERAS
        elif brand_series == 'DX':
            return NIKON_DX_CAMERAS
        elif brand_series == 'FX':
            return NIKON_FX_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Olympus':
        if brand_series == 'E series':
            return OLYMPUS_E_SERIES_CAMERAS
        elif brand_series == 'O-MD':
            return OLYMPUS_OMD_CAMERAS
        elif brand_series == 'PEN':
            return OLYMPUS_PEN_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Panasonic':
        if brand_series == 'Lumix G':
            return PANASONIC_LUMIX_G_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Pentax':
        if brand_series == 'K series':
            return PENTAX_K_SERIES_CAMERAS
        elif brand_series == 'Q series':
            return PENTAX_Q_SERIES_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Samsung':
        if brand_series == 'NX':
            return SAMSUNG_NX_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    elif brand == 'Sony':
        if brand_series == 'A-mount':
            return SONY_A_MOUNT_CAMERAS
        elif brand_series == 'E-mount':
            return SONY_E_MOUNT_CAMERAS
        elif brand_series == 'FE-mount':
            return SONY_FE_MOUNT_CAMERAS
        else:
            print("No match, this shouldnt ever happen. Exiting with error...")
            sys.exit(1)

    else:
        print("Sorry no matches for this, this should never happen, going to exit now with error.")
        sys.exit(1)


def lookup_lens_asins_for_cam(brand, brand_series, brand_model):
    url = "http://www.amazon.com/gp/finders/ajax/finderajax.html?action=getSupplies&finderId=lens&nodeId=" + brand + "%5E" + brand_series.replace(" ", "+") + "%5E" + brand_model.replace(" ", "+") + "&supplyPage=1&pageSize=999&refinements=&supplyBrand=&redir=pf_rd_p%3D1561025342%26pf_rd_s%3Dcenter-5%26pf_rd_t%3D101%26pf_rd_i%3D6207565011%26pf_rd_m%3DATVPDKIKX0DER%26pf_rd_r%3D0B8F6QAY4MYB29EFZS0H&PowerBar=0"
    try:
        r = requests.get(url, headers=r_headers)
        soup = BeautifulSoup(r.text)
        asins = re.findall(r'"ASIN":"(\w+)"', str(soup.prettify()))
        return asins
    except:
        print("Couldnt return asins for " + brand + " " + brand_model)

"""
def amazon_query_asin(asin):
    try:
        response = amazon.ItemLookup(ItemId=asin)
    except:
        print("error performing amazon lookup of " + asin)
        sys.exit(1)
    try:
        soup = BeautifulSoup(response)
    except:
        print("error creating soup from response.")
    return soup
"""

"""
    response = amazon.ItemLookup(ItemId=asin)
    soup = BeautifulSoup(response)
    return unicode(soup)
"""


"""
def re_lens_title(title_long):
    try:
        title = re.search(r"(^.*?) Lens for", title_long).group(1)
        print("regex match - title set to " + title)
    except:
        title = str(title_long)
        print("no regex match - title set to " + title)
    return title
"""


class Command(BaseCommand):
    def handle(self, **options):
        for brand in CAMERA_BRANDS:
            for brand_series in list_brand_series(brand=brand):
                for brand_model in list_brand_series_models(brand=brand,brand_series=brand_series):
                    #print(brand + " " + brand_series + " " + brand_model)
                    asins = lookup_lens_asins_for_cam(brand=brand, brand_series=brand_series, brand_model=brand_model)
                    for asin in asins:
                        print(asin)

                    time.sleep(3)

"""
                for model_name in get_series_models(brand=brand, brand_series=brand_series):
                    cam_title = brand + " " + model_name
                    print(cam_title)
                    try:
                        c = Camera.objects.get(title=cam_title)
                        print("Matched on " + cam_title)
                    except:
                        print("No match for " + cam_title + " creating...")
                        c = Camera.objects.create(title=cam_title, brand=CameraBrand.objects.get(title=brand))


                    asins = lookup_lens_asins_for_cam(brand=brand, brand_series=brand_series, model_name=model_name)
                    for asin in asins:
                        print("Checking if ASIN already exists... " + asin)
                        try:
                            l = CameraLens.objects.get(amazon_asin=asin)
                        except:
                            print("Lens with ASIN " + asin + " doesnt already exist, querying amazon and creating.")

                            soup = amazon_query_asin(asin=asin)
                            try:
                                title_long = soup.find("title").text
                                title = unicode(title_long)
                                #title = re_lens_title(title_long)
                            except:
                                print("errored the fucking souping title_long text...")
                                print(soup)

                            try:
                                amazon_detail_page_url = unicode(soup.find("detailpageurl").text)
                            except:
                                print("error getting amazon detail page, setting it to blank")
                                amazon_detail_page_url = ""

                            try:
                                l = CameraLens.objects.get_or_create(title=title, amazon_asin=asin,amazon_detail_page_url=amazon_detail_page_url)
                            except:
                                print("Error: Failed to get or create CameraLens object...")
                                #sys.exit(1)
                        try:
                            c.lenses.add(l)
                        except:
                            print("Something fucked up adding lens to camera")
                            #sys.exit(1)

                        print("looks like we made it through, sleeping for a bit then we go again...")

                        sleep_time = random.randint(5,6)
                        time.sleep(sleep_time)
"""
