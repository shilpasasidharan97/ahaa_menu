# Generated by Django 4.1.3 on 2022-11-21 06:49

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("website", "0003_alter_cartitems_quantity")]

    operations = [migrations.AddField(model_name="cartitems", name="total", field=models.FloatField(default=1, null=True))]
