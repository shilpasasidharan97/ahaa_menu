# Generated by Django 4.1.3 on 2022-12-01 05:33

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("website", "0012_socialmedialink")]

    operations = [migrations.AddField(model_name="restaurant", name="is_table", field=models.BooleanField(default=True))]
