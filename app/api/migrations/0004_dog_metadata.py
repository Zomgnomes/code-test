# Generated by Django 4.0.5 on 2022-06-06 21:41
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_modifieddog"),
    ]

    operations = [
        migrations.AddField(
            model_name="dog",
            name="metadata",
            field=models.JSONField(blank=True, null=True),
        ),
    ]