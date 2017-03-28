from __future__ import unicode_literals
import time

import bottlenose
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from camera_lens.models import CameraLens

AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
AWS_ASSOCIATE_TAG=''

amazon = bottlenose.Amazon(AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG)


class Command(BaseCommand):


    def handle(self, **options):
        lenses = CameraLens.objects.all()
        for l in lenses:
            if not l.amazon_asin:
                print(l.title + " doesnt have an asin, cant lookup amazon review iframe.")
            else:
                print(l.title + " has a fucking asin... proceeding.")
                if not l.amazon_review_iframe_url:
                    print("review iframe not fucking populated, sending request to amazon.")

                    try:
                        response = amazon.ItemLookup(ItemId=str(l.amazon_asin), ResponseGroup="Reviews")
                        soup = BeautifulSoup(response)

                        amazon_review_iframe_url = soup.find("iframeurl").text
                        l.amazon_review_iframe_url = amazon_review_iframe_url

                        print(l.amazon_review_iframe_url)

                        l.save()
                        print("made it through this fucking round, sleeping for 3 then we go again.")
                        time.sleep(3)

                    except:
                        print("error souping or performing the fucking amazon lookup of " + l.title)

                    time.sleep(2)

                else:
                    print("already fucking populated, moving on.")
                    time.sleep(1)


"""
response = amazon.ItemLookup(ItemId=AMAZON_ASIN, ResponseGroup="Reviews")
soup = BeautifulSoup(response)
print(soup.prettify())
"""
