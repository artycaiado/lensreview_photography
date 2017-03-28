from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import re

from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django_extensions.db.models import TimeStampedModel,TitleSlugDescriptionModel


CAMERA_LENS_BRANDS = (
    ('CAN', 'Canon'),
    ('NIK', 'Nikon'),
    ('SON', 'Sony'),
    ('TAM', 'Tamron'),
    ('TOK', 'Tokina'),
    ('SIG', 'Sigma'),
    ('SAM', 'Samsung'),
    ('PEN', 'Pentax'),
    ('PAN', 'Panasonic'),
    ('OLY', 'Olympus'),
    ('SNG', 'Samyang'),
    ('ROK', 'Rokinon'),
    ('LEI', 'Leica'),
    ('FUJ', 'Fuji'),
    ('VOI', 'Voigtlander'),
    ('NIL', 'Not Specified')
)


SENSOR = (
    ('CROP', 'Crop'),
    ('FULL', 'Full Frame')
)

SENSOR_NAME = (
    ('APS-C', 'Nikon Crop'),
    ('EF', 'Canon Full-frame'),
    ('EF-S', 'Canon Crop'),
    ('DG', 'Sigma Full-frame'),
    ('DC', 'Sigma Crop'),
    ('Di', 'Tamron Full-frame'),
    ('Di-II', 'Tamron Crop'),
    ('DT', 'Sony Crop')
)

IMAGE_STABILIZATION = (
    ('IS', 'Canon IS'),
    ('IS2', 'Canon IS II'),
    ('VR', 'Nikon VR'),
    ('VR2', 'Nikon VR II'),
    ('VC', 'Tamron VC'),
    ('OS', 'Sigma Optical Stabilization'),
    ('OIS', 'Panasonic/Mega Optical Image Stabilization'),
    ('OSS', 'Sony OSS'),
    ('OSSA', 'Sony OSS Active'),
    ('SOIS', 'Samsung OIS'),
    ('NONE', 'None')
)


FOCUS_MOTOR = (

    ('AFS', 'Nikon AF-S - Auto Focus Silent also known as Silent Wave Motor or SWM'),
    ('USM', 'Canon USM - Ultra Sonic Motor'),
    ('STM', 'Canon STM - Stepping Motor which is better for video'),
    ('HSM', 'Sigma HSM - Hyper Sonic Motor'),
    ('USD', 'Tamron USD - Ultrasonic Silent Drive'),
    ('PZD', 'Tamron PZD  - Peizo Drive'),
    ('SWD', 'Olympus SWD - Supersonic Wave Drive'),
    ('SSM', 'Sony SSM - Supersonic Wave Motor'),
    ('SAM', 'Sony SAM - Smooth Autofocus Motor - not silent like SSM'),
    ('SDM', 'Pentax SDM - Supersonic Drive Motor'),
    ('GEN', 'Generic')

)


# portrait - 50mm 85mm fixed typically are better to shoot people without distorting, wide angle lenses distort
# Wide-Angle -
# landscape - typically wide-angle
# telephoto - zoom...
# low light - very high aperture (low f-stop number)
# wildlife - super telephoto, long zoom
# macro - good at shooting items close up without distortion, a lot of crossover with portrait?
# sports - quick shutter speed
# fisheye - cool for more abstract/artistic thought usually, lots of distortion
# travel - good all around lens
# tilt-shift
LENS_CATEGORY = (
    ('FYE', 'Fisheye'),
    ('WA', 'Wide-Angle'),
    ('UWZ', 'Ultra-Wide Zoom'),
    ('SZ', 'Standard Zoom'),
    ('TZ', 'Telephoto Zoom'),
    ('STD', 'Standard Telephoto'),
    ('MT', 'Medium Telephoto'),
    ('STZ', 'Super Telephoto Zoom'),
    ('MAC', 'Macro'),
    ('TSH', 'Tile-Shift')
)

# models.manytomanyfield for category

# Nikon 1
# Nikon F
# Nikon FX
# Canon EF
# Canon EF (Full-frame)
# Canon EF-S
# Canon EF-M
# Sony E
# Sony Alpha
# Sony Alpha (Full-frame)
# Sony Alpha DT
# Pentax K
# Sigma SA
# Leica M
# Fuji X
# Micro Four Thirds
# Four Thirds
# Samsung NX
"""
LENS_MOUNTS = (
    ()
)
"""

PRO_SERIES = (
    ('L', 'Canon Luxury'),
    ('EX', 'Sigma EX Lens'),
    ('SP', 'Tamron SP Superior Performance'),
    ('DA', 'Pentax DA'),
    ('G', 'Sony G'),
    ('ZA', 'Sony ZA - Zeiss-designed'),
)

FOCUS_TECH = (
    ('IF', 'Inner-Focus'),
    ('RF', 'Rear-Focus'),
    ('FL', 'Floating System'),
)

GLASS_TECH = (
    ('', ''),
)

GLASS_COATING = (
    ('AS', 'Hingo'),
)

class CameraLensManager(models.Manager):


    def lens_brand_count(self, keyword):
        return self.filter(lens_brand__icontains=keyword).count()


@python_2_unicode_compatible
class CameraLens(TimeStampedModel,TitleSlugDescriptionModel):
    lens_brand = models.CharField(max_length=3, choices=CAMERA_LENS_BRANDS)
    lens_pro_series = models.CharField(max_length=3, choices=PRO_SERIES, blank=True)
    lens_msrp = models.CharField(max_length=20, blank=True)

    lens_zoom = models.CharField(max_length=10, blank=True)
    focal_length_min = models.IntegerField(null=True, blank=True)
    focal_length_max = models.IntegerField(null=True, blank=True)

    aperture_wide_max = models.FloatField(null=True, blank=True)
    aperture_wide_min = models.FloatField(null=True, blank=True)
    aperture_zoom_max = models.FloatField(null=True, blank=True)
    aperture_zoom_min = models.FloatField(null=True, blank=True)

    lens_sensor = models.CharField(max_length=4, choices=SENSOR, blank=True)
    lens_sensor_name = models.CharField(max_length=6, choices=SENSOR_NAME, blank=True)

    image_stabilization = models.CharField(max_length=8, choices=IMAGE_STABILIZATION, blank=True)
    focus_motor = models.CharField(max_length=3, choices=FOCUS_MOTOR, blank=True)
    focus_technology = models.CharField(max_length=3, choices=FOCUS_TECH, blank=True)

    glass_technology = models.CharField(max_length=4, choices=GLASS_TECH, blank=True)
    glass_coating = models.CharField(max_length=4, choices=GLASS_COATING, blank=True)

    filter_size = models.IntegerField(null=True, blank=True)
    lens_length = models.IntegerField(null=True, blank=True)
    lens_weight = models.IntegerField(null=True, blank=True)
    lens_diameter = models.IntegerField(null=True, blank=True)

    amazon_title = models.CharField(max_length=255, blank=True)
    amazon_asin = models.CharField(max_length=24, blank=True)
    amazon_detail_page_url = models.URLField(max_length=512, blank=True)
    amazon_review_page_url = models.URLField(max_length=512, blank=True)
    amazon_review_iframe_url = models.URLField(max_length=1024, blank=True)

    amazon_image_thumb_sm = models.URLField(blank=True)
    amazon_image_thumb_lg = models.URLField(blank=True)
    amazon_image_sm = models.URLField(blank=True)
    amazon_image_md = models.URLField(blank=True)
    amazon_image_lg = models.URLField(blank=True)

    product_thumb_sm_url = models.URLField(blank=True)
    product_thumb_lg_url = models.URLField(blank=True)

    dpreview_url = models.URLField(blank=True)
    photography_blog_test_url = models.URLField(blank=True)
    photography_blog_news_url = models.URLField(blank=True)
    lensdatabase_net_detail_url = models.URLField(blank=True)


    objects = CameraLensManager()


    class Meta:
        verbose_name = "lens"
        verbose_name_plural = "lenses"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.lens_brand:
            if re.search(r'Tamron', self.title):
                self.lens_brand = "TAM"
            elif re.search(r'Tokina', self.title):
                self.lens_brand = "TOK"
            elif re.search(r'Sigma', self.title):
                self.lens_brand = "SIG"
            elif re.search(r'Samyang', self.title):
                self.lens_brand = "SNG"
            elif re.search(r'Rokinon', self.title):
                self.lens_brand = "ROK"
            elif re.search(r'Voigtlander', self.title):
                self.lens_brand = "VOI"
            elif re.search(r'Pentax', self.title):
                self.lens_brand = "PEN"
            elif re.search(r'PENTAX', self.title):
                self.lens_brand = "PEN"
            elif re.search(r'Fujifilm', self.title):
                self.lens_brand = "FUJ"
            elif re.search(r'Fujinon', self.title):
                self.lens_brand = "FUJ"
            elif re.search(r'Panasonic', self.title):
                self.lens_brand = "PAN"
            elif re.search(r'Olympus', self.title):
                self.lens_brand = "OLY"
            elif re.search(r'Zuiko', self.title):
                self.lens_brand = "OLY"
            elif re.search(r'Samsung', self.title):
                self.lens_brand = "SAM"
            elif re.search(r'Leica', self.title):
                self.lens_brand = "LEI"
            elif re.search(r'Canon', self.title):
                self.lens_brand = "CAN"
            elif re.search(r'Nikon', self.title):
                self.lens_brand = "NIK"
            elif re.search(r'Sony', self.title):
                self.lens_brand = "SON"
            elif re.search(r'SONY', self.title):
                self.lens_brand = "SON"
            else:
                self.lens_brand = "NIL"

        # and if not self.focal_length_min ...
        if not self.focal_length_max:
            try:
                focal_length_variable = re.search(r'(\d+)-(\d+)mm', self.title)
                self.focal_length_min = int(focal_length_variable.group(1))
                self.focal_length_max = int(focal_length_variable.group(2))
            except:
                try:
                    focal_length_fixed = re.search(r'(\d+)mm', self.title)
                    self.focal_length_min = int(focal_length_fixed.group(1))
                    self.focal_length_max = int(focal_length_fixed.group(1))
                except:
                    pass

        # and if not self.aperture_zoom_max
        if not self.aperture_wide_max:
            try:
                aperture = re.search(r'f/(\d+.\d+)-(\d+.\d+)', self.title)
                self.aperture_wide_max = float(aperture.group(1))
                self.aperture_zoom_max = float(aperture.group(2))
            except:
                try:
                    aperture = re.search(r'f/(\d+.\d+)-(\d+)', self.title)
                    self.aperture_wide_max = float(aperture.group(1))
                    self.aperture_zoom_max = float(aperture.group(2))
                except:
                    try:
                        aperture = re.search(r'f/(\d+)-(\d+.\d+)', self.title)
                        self.aperture_wide_max = float(aperture.group(1))
                        self.aperture_zoom_max = float(aperture.group(2))
                    except:
                        try:
                            aperture = re.search(r'f/(\d+.\d+)', self.title)
                            self.aperture_zoom_max = float(aperture.group(1))
                            self.aperture_wide_max = float(aperture.group(1))
                        except:
                            try:
                                aperture = re.search(r'f/(\d+)', self.title)
                                self.aperture_zoom_max = float(aperture.group(1))
                                self.aperture_wide_max = float(aperture.group(1))
                            except:
                                try:
                                    aperture = re.search(r'F/(\d+.\d+)-(\d+.\d+)', self.title)
                                    self.aperture_wide_max = float(aperture.group(1))
                                    self.aperture_zoom_max = float(aperture.group(2))
                                except:
                                    try:
                                        aperture = re.search(r'F/(\d+.\d+)-(\d+)', self.title)
                                        self.aperture_wide_max = float(aperture.group(1))
                                        self.aperture_zoom_max = float(aperture.group(2))
                                    except:
                                        try:
                                            aperture = re.search(r'F/(\d+)-(\d+.\d+)', self.title)
                                            self.aperture_wide_max = float(aperture.group(1))
                                            self.aperture_zoom_max = float(aperture.group(2))
                                        except:
                                            try:
                                                aperture = re.search(r'F/(\d+.\d+)', self.title)
                                                self.aperture_zoom_max = float(aperture.group(1))
                                                self.aperture_wide_max = float(aperture.group(1))
                                            except:
                                                try:
                                                    aperture = re.search(r'F/(\d+)', self.title)
                                                    self.aperture_zoom_max = float(aperture.group(1))
                                                    self.aperture_wide_max = float(aperture.group(1))
                                                except:
                                                    try:
                                                        aperture = re.search(r'F(\d+.\d+)-(\d+.\d+)', self.title)
                                                        self.aperture_wide_max = float(aperture.group(1))
                                                        self.aperture_zoom_max = float(aperture.group(2))
                                                    except:
                                                        try:
                                                            aperture = re.search(r'F(\d+.\d+)-(\d+)', self.title)
                                                            self.aperture_wide_max = float(aperture.group(1))
                                                            self.aperture_zoom_max = float(aperture.group(2))
                                                        except:
                                                            try:
                                                                aperture = re.search(r'F(\d+)-(\d+.\d+)', self.title)
                                                                self.aperture_wide_max = float(aperture.group(1))
                                                                self.aperture_zoom_max = float(aperture.group(2))
                                                            except:
                                                                try:
                                                                    aperture = re.search(r'F(\d+.\d+)', self.title)
                                                                    self.aperture_zoom_max = float(aperture.group(1))
                                                                    self.aperture_wide_max = float(aperture.group(1))
                                                                except:
                                                                    try:
                                                                        aperture = re.search(r'F(\d+)', self.title)
                                                                        self.aperture_zoom_max = float(aperture.group(1))
                                                                        self.aperture_wide_max = float(aperture.group(1))
                                                                    except:
                                                                        try:
                                                                            aperture = re.search(r'f(\d+.\d+)-(\d+.\d+)', self.title)
                                                                            self.aperture_wide_max = float(aperture.group(1))
                                                                            self.aperture_zoom_max = float(aperture.group(2))
                                                                        except:
                                                                            try:
                                                                                aperture = re.search(r'f(\d+.\d+)-(\d+)', self.title)
                                                                                self.aperture_wide_max = float(aperture.group(1))
                                                                                self.aperture_zoom_max = float(aperture.group(2))
                                                                            except:
                                                                                try:
                                                                                    aperture = re.search(r'f(\d+)-(\d+.\d+)', self.title)
                                                                                    self.aperture_wide_max = float(aperture.group(1))
                                                                                    self.aperture_zoom_max = float(aperture.group(2))
                                                                                except:
                                                                                    try:
                                                                                        aperture = re.search(r'f(\d+.\d+)', self.title)
                                                                                        self.aperture_zoom_max = float(aperture.group(1))
                                                                                        self.aperture_wide_max = float(aperture.group(1))
                                                                                    except:
                                                                                        try:
                                                                                            aperture = re.search(r'f(\d+)', self.title)
                                                                                            self.aperture_zoom_max = float(aperture.group(1))
                                                                                            self.aperture_wide_max = float(aperture.group(1))
                                                                                        except:
                                                                                            self.aperture_zoom_max = None
                                                                                            self.aperture_wide_max = None


        if not self.image_stabilization:
            if re.search(r'IS II', self.title):
                self.image_stabilization = "IS2"
            elif re.search(r'IS', self.title):
                self.image_stabilization = "IS"
            elif re.search(r'VR II', self.title):
                self.image_stabilization = "VR2"
            elif re.search(r'VR', self.title):
                self.image_stabilization = "VR"
            elif re.search(r'VC', self.title):
                self.image_stabilization = "VC"
            elif re.search(r'OS', self.title):
                self.image_stabilization = "OS"
            elif re.search(r'OIS', self.title):
                self.image_stabilization = "OIS"
            elif re.search(r'OSS', self.title):
                self.image_stabilization = "OSS"
            elif re.search(r'OSSA', self.title):
                self.image_stabilization = "OSSA"
            elif re.search(r'SOIS', self.title):
                self.image_stabilization = "SOIS"
            else:
                pass

        if not self.focus_motor:
            if re.search(r'AF-S', self.title):
                self.focus_motor = "AFS"
            elif re.search(r'USM', self.title):
                self.focus_motor = "USM"
            elif re.search(r'STM', self.title):
                self.focus_motor = "STM"
            elif re.search(r'HSM', self.title):
                self.focus_motor = "HSM"
            elif re.search(r'USD', self.title):
                self.focus_motor = "USD"
            elif re.search(r'PZD', self.title):
                self.focus_motor = "PZD"
            elif re.search(r'SWD', self.title):
                self.focus_motor = "SWD"
            elif re.search(r'SSM', self.title):
                self.focus_motor = "SSM"
            elif re.search(r'SAM', self.title):
                self.focus_motor = "SAM"
            elif re.search(r'SDM', self.title):
                self.focus_motor = "SDM"
            else:
                pass


        """
        if not self.lens_zoom:
            try:
                self.lens_zoom = str(float(self.focal_length_max) / float(self.focal_length_min))[:10]
            except:
                pass
        """

        super(CameraLens, self).save(*args, **kwargs)


    def get_absolute_url(self):
        slug = self.slug
        return reverse("lens-detail", kwargs={"slug": slug})


    # code shows what this is, but make a page to show all prime lenses vs zoom, and put description at top of what that is.
    def is_prime(self):
        if self.focal_length_min == self.focal_length_max:
            return True
        else:
            return False


    def is_zoom(self):
        if not self.focal_length_min == self.focal_length_max:
            return True
        else:
            return False


    def __str__(self):
        return self.title


"""

# Automatically populate ImageFile from URL
# try to rename as slug-thumb_sm slug-sm slug-md, etc.
# still serve from remote servers, can move to local copy if ever
# necessary

# if this method added, add get_remote_image() to def save

from django.core.files import File
import os

class Item(models.Model):
    image_file = models.ImageField(upload_to='images')
    image_url = models.URLField()


    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0]))
                    )
            self.save()
"""


class CameraLensExamplePhoto(models.Model):
    camera_lens = models.ForeignKey(CameraLens, related_name='example_photos')
    image = models.ImageField(upload_to='example_photos')


class CameraLensProductPhoto(models.Model):
    camera_lens = models.ForeignKey(CameraLens, related_name='product_photos')
    image = models.ImageField(upload_to='product_photos')


"""
>>> n = CameraLens.objects.lens_brand_count('NIK')
>>> print(n)
2
>>> n = CameraLens.objects.lens_brand_count('SIG')
>>> print(n)
3
>>> n = CameraLens.objects.lens_brand_count('')
>>> print(n)
15
"""
