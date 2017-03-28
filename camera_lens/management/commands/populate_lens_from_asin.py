#/usr/bin/env python

import random
import re
import requests
import sys
import time

import bottlenose
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand, CommandError
from django.utils.safestring import SafeUnicode

from camera_lens.models import CameraLens



AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
AWS_ASSOCIATE_TAG=''

amazon = bottlenose.Amazon(AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG)


try:
    sys.argv[2]
except IndexError:
    print("")
    print("------------------------------------------------")
    print("Need to supply an ASIN")
    print("./manage.py populate_lens_from_asin ASIN1234")
    print("------------------------------------------------")
    print("")
    sys.exit(1)


asin = sys.argv[2]



def check_if_lens_with_asin_already_exists(asin):
    print("Checking if lens already exists in database")
    try:
        lens = CameraLens.objects.get(amazon_asin=asin)
    except CameraLens.DoesNotExist:
        lens = None

    if lens:
        return True
    else:
        return False

"""
    try:
        l = CameraLens.objects.get(amazon_asin=asin)
        return True
    except:
        print("Did not find lens with asin " + asin)
        return False
"""

def amazon_query_asin(asin):

    print("Querying amazon api...")
    try:
        response = amazon.ItemLookup(ItemId=asin)
    except:
        print("error performing amazon lookup of " + asin)

    print("Parsing the response.")
    try:
        soup = BeautifulSoup(response)
    except:
        print("error creating soup from response.")

    return soup



class Command(BaseCommand):
    args = sys.argv[2]
    help = 'Feed this a CameraLens ASIN and it will populate lenses.'

    def handle(self, *args, **options):
        asin = args[0]
        print(SafeUnicode(asin))

        if check_if_lens_with_asin_already_exists(asin):
            print("Already exists...")

        else:
            print("This lens does not exist, lets create it.")
            soup = amazon_query_asin(asin)
            print("Setting the title from parsed results.")
            try:
                title = SafeUnicode(soup.find("title").text).replace(u'\xa0', ' ').encode('utf-8')
            except:
                print("errored the setting of title.")

            """
            print("getting detail page url")
            try:
                amazon_detail_page_url = SafeUnicode(soup.find("detailpageurl").text)
                print(amazon_detail_page_url)
            except:
                print("error getting amazon detail page, setting it to blank")
                amazon_detail_page_url = ""
            """

            if title:
                print("Creating CameraLens - " + title)

            try:
                lens = CameraLens.objects.create(title=title, amazon_asin=asin)
            except:
                print("Error: Failed to create CameraLens object...")

            #print(soup.prettify())
