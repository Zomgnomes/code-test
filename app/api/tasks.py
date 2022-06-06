import json
from io import BytesIO
from urllib.request import urlopen

from django.core.files.images import File
from django.core.files.temp import NamedTemporaryFile
from PIL import ExifTags
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .models import Dog
from .models import ModifiedDog
from app.celery import app


@app.task(name="get_dogs")
def get_dogs():
    url = "https://dog.ceo/api/breed/pug/images/random/24"
    with urlopen(url) as url_open_response:
        assert url_open_response.status == 200
        dog_urls = json.loads(url_open_response.read().decode()).get("message")
        for dog_url in dog_urls:
            new_dog = Dog()
            new_dog.source_url = dog_url
            new_dog.save()
            load_dog_image.delay(new_dog.id)
        return dog_urls


@app.task(name="load_dog_image")
def load_dog_image(dog_id):
    dog = Dog.objects.get(pk=dog_id)
    temporary_image = NamedTemporaryFile(delete=True)
    with urlopen(dog.source_url) as url_open_response:
        assert url_open_response.status == 200
        temporary_image.write(url_open_response.read())
        temporary_image.flush()

    # Pillow kind of sucks at getting EXIF metadata but setting up ExifTool
    # and getting it to play nice with the Alpine docker seems like overkill
    # especially after fighting with the LocalStack docker
    # EXIF data is at least preserved on the image itself if you need it
    # Switching to Pillow==7.0.0 seems to get more EXIF data so that's my
    # "good enough" solution for this, though all of the API images don't
    # actually have any EXIF data, so that kind of sucks too
    exifdata = Image.open(File(temporary_image)).getexif()
    metadata = {}
    for tag_id in exifdata:
        tag = "Unknown Exif Tag"
        if tag_id in ExifTags.TAGS:
            tag = ExifTags.TAGS.get(tag_id)
        elif tag_id in ExifTags.GPSTAGS:
            tag = ExifTags.GPSTAGS.get(tag_id)
        data = str(exifdata.get(tag_id))
        metadata[tag] = data
    dog.image.save(f"dog{dog.id}.jpg", File(temporary_image))
    dog.metadata = metadata
    dog.save()
    modify_dog.delay(dog.id)


@app.task(name="modify_dog")
def modify_dog(dog_id):
    dog = Dog.objects.get(pk=dog_id)
    new_image = Image.open(dog.image).rotate(180)
    drawing = ImageDraw.Draw(new_image)
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS_Bold.ttf", 72
    )
    drawing.text((10, 10), "What's Up Dog?", font=font, fill=(255, 255, 255))

    blob = BytesIO()
    new_image.save(blob, "JPEG")
    modified_dog = ModifiedDog(source_dog=dog)
    modified_dog.modified_image.save(f"modified_dog{dog.id}.jpg", File(blob))
    modified_dog.save()
