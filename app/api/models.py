from django.db import models


class Key(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    counter = models.BigIntegerField()