from django.db import models


class Key(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    counter = models.BigIntegerField()

    def increment(self, by=1):
        self.counter += by
        self.save()


class Dog(models.Model):
    image = models.ImageField(upload_to="dogs/", null=True, blank=True)
    source_url = models.URLField(max_length=1024, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)


class ModifiedDog(models.Model):
    source_dog = models.OneToOneField(
        Dog,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    modified_image = models.ImageField(
        upload_to="modified_dogs/", null=True, blank=True
    )
