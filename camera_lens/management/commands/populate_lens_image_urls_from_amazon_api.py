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
                print(l.title + " doesnt have a fucking asin, cant lookup photos.")
            else:
                print(l.title + " has an asin... proceeding.")
                if not l.amazon_image_thumb_sm:
                    print("images not populated, sending request to amazon.")

                    try:
                        response = amazon.ItemLookup(ItemId=str(l.amazon_asin), ResponseGroup="Images")
                        soup = BeautifulSoup(response)

                        # -- swiatchimage 30x27
                        swatchimage = soup.find("swatchimage")
                        amazon_image_thumb_sm = swatchimage.find("url").text
                        l.amazon_image_thumb_sm = amazon_image_thumb_sm
                        print(l.amazon_image_thumb_sm)

                        thumbnailimage = soup.find("thumbnailimage")
                        amazon_image_thumb_lg = thumbnailimage.find("url").text
                        l.amazon_image_thumb_lg = amazon_image_thumb_lg
                        print(l.amazon_image_thumb_lg)

                        tinyimage = soup.find("tinyimage")
                        amazon_image_sm = tinyimage.find("url").text
                        l.amazon_image_sm = amazon_image_sm
                        print(l.amazon_image_sm)

                        mediumimage = soup.find("mediumimage")
                        amazon_image_md = mediumimage.find("url").text
                        l.amazon_image_md = amazon_image_md
                        print(l.amazon_image_md)

                        largeimage = soup.find("largeimage")
                        amazon_image_lg = largeimage.find("url").text
                        l.amazon_image_lg = amazon_image_lg
                        print(l.amazon_image_lg)

                        l.save()
                        print("made it through this fucking round, sleeping for 3 then we go again.")
                        time.sleep(3)

                    except:
                        print("error souping or performing the fucking amazon lookup of " + l.title)

                    time.sleep(2)

                else:
                    print("already populated, moving on.")
                    time.sleep(1)
