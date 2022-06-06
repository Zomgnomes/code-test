import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Key
from .models import ModifiedDog
from .serializers import KeySerializer
from .tasks import get_dogs


@api_view(["GET"])
# Lists all keys and counter values
def key_list(request, format=None):
    keys = Key.objects.all().order_by("name")
    serializer = KeySerializer(keys, many=True)
    return Response(serializer.data)


# Allows for getting a specific key, creating new keys, incrementing keys, and deleting keys
@api_view(["POST", "GET", "PUT", "DELETE"])
def key_specific(request, name, format=None):
    # Get a specific key
    try:
        key = Key.objects.get(pk=name)
    except Key.DoesNotExist:
        # Handle creating new keys for the post route if we hit a not found and it's a post
        if request.method == "POST":
            if len(name) <= 100:
                new_key = Key(name=name, counter=0)
                new_key.save()
                serializer = KeySerializer(new_key)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # If the key name is too long for our field throw it out
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # If it's not a POST and it's not found complain about it
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        # Handle POST requests if it already exists
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        # Serialize and spit out the specific key
        serializer = KeySerializer(key)
        return Response(serializer.data)
    elif request.method == "PUT":
        # Increment the key if it exists
        key.increment()
        serializer = KeySerializer(key)
        return Response(serializer.data)
        pass
    # Delete the key if it exists
    elif request.method == "DELETE":
        key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
# Load two dozen dog images into the system
def dog_load(request, format=None):
    try:
        get_dogs.delay().get()
        return Response(status=status.HTTP_201_CREATED)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# Return the image urls for the two dogs they want
def dog_output(request, format=None):
    all_dogs = ModifiedDog.objects.all()
    if all_dogs.count() > 0:
        modified_dog = random.choice(all_dogs)
        data = {
            "original": modified_dog.source_dog.image.url,
            "modified": modified_dog.modified_image.url,
            "metadata": modified_dog.source_dog.metadata,
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
