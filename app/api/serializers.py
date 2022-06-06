from rest_framework import serializers

from .models import Dog
from .models import Key


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = [
            "name",
            "counter",
        ]


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = [
            "id",
            "image",
            "source_url",
        ]
