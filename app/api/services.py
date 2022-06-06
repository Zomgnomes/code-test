import json
from urllib.request import urlopen

from .models import Dog


def get_dogs():
    url = "https://dog.ceo/api/breed/pug/images/random/12"
    with urlopen(url) as url_open_response:
        assert url_open_response.status == 200
        dog_urls = json.loads(url_open_response.read().decode()).get("message")
        for dog_url in dog_urls:
            new_dog = Dog()
            new_dog.get_image_from_url(dog_url)
        return dog_urls
