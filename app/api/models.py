from urllib.request import urlopen

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models


class Key(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    counter = models.BigIntegerField()

    def increment(self, by=1):
        self.counter += by
        self.save()


class Dog(models.Model):
    image = models.ImageField(upload_to="dogs/", null=True, blank=True)
    source_url = models.URLField(blank=True, null=True)

    def get_image_from_url(self, url):
        temporary_image = NamedTemporaryFile(delete=True)
        with urlopen(url) as url_open_response:
            assert url_open_response.status == 200
            temporary_image.write(url_open_response.read())
            temporary_image.flush()
        image = File(temporary_image)
        filename = url.split("/")[-1]
        self.image.save(filename, image)
        self.source_url = url
        self.save()
