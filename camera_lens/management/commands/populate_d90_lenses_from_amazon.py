import re
import requests
import sys
import time

import bottlenose
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from camera_lens.models import CameraLens
from camera.models import Camera

AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
AWS_ASSOCIATE_TAG=''

amazon = bottlenose.Amazon(AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG)


def get_camera():
    # make this take an argument of title and maybe get_or_create, also add
    # check for CameraBrand and get_or_create that
    try:
        c = Camera.objects.get(title="Nikon D90")
    except:
        print("Something fucked up getting the camera ")
        sys.exit(1)
    return c


def get_lens_asins_for_camera():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    # d90 url, gotten through chrome debug console, network tab when using lens finder on amazon
    url = "http://www.amazon.com/gp/finders/ajax/finderajax.html?action=getSupplies&finderId=lens&nodeId=Nikon%5EDX%5ED7100&supplyPage=1&pageSize=96&refinements=&supplyBrand=&redir=pf_rd_p%3D1561025342%26pf_rd_s%3Dcenter-5%26pf_rd_t%3D101%26pf_rd_i%3D6207565011%26pf_rd_m%3DATVPDKIKX0DER%26pf_rd_r%3D0RFHH75KVEN6KTKCF187&PowerBar=0"
    r = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(r.text)
    asins = re.findall(r'"ASIN":"(\w+)"', str(soup.prettify()))
    return asins


def amazon_query_asin(asin):
    # maybe add some try logic here to see if lens already exists in db
    # before sending request to amazon
    try:
        response = amazon.ItemLookup(ItemId=str(asin))
    except:
        print("error performing amazon lookup of " + asin)
        sys.exit(1)
    try:
        soup = BeautifulSoup(response)
    except:
        print("error creating soup from response.")
    return soup


def re_lens_title(title_long):
    try:
        title = re.search(r"(^.*?) Lens for", title_long).group(1)
        print("regex match - title set to " + title)
    except:
        title = str(title_long)
        print("no regex match - title set to " + title)
    return title


class Command(BaseCommand):


    def handle(self, **options):
        d90 = get_camera()
        asins = get_lens_asins_for_camera()

        for asin in asins:
            # add try/except for objects.get for asin, don't query if lens already exists,
            # just add it to camera in that case... maybe combine amazon_query_asin
            # with get_or_create_lens_from_amazon(asin) that returns the lens

            soup = amazon_query_asin(asin)
            try:
                title_long = soup.find("title").text
                title = re_lens_title(title_long)
            except:
                print("errored the fucking souping title_long text...")
                print(soup)

            try:
                amazon_detail_page_url = str(soup.find("detailpageurl").text)
            except:
                print("error getting amazon detail page, setting it to blank")
                amazon_detail_page_url = ""

            try:
                l = CameraLens.objects.get(amazon_asin=asin)
            except:
                try:
                    l = CameraLens.objects.create(title=title, amazon_asin=asin,amazon_detail_page_url=amazon_detail_page_url)
                except:
                    print("Failed to get or create CameraLens object...")
                    sys.exit(1)

            try:
                d90.lenses.add(l)
            except:
                print("Something fucked up adding lens to d90.")
                sys.exit(1)

            print("looks like we made it through, sleeping for 5 seconds then we go again...")
            time.sleep(5)




"""
                if created:
                    print("Created: " + title + r)
                else:
                    print("Looks like " + title + " already exists here.")

                print("Adding " + title + " with ASIN " + amazon_asin + "to " + d90.title)


                # add a sleep so we don't hammer the api servers and get blocked
            except:
                print("Something fucked up with this one, but no need to freak out and fail.")

"""
