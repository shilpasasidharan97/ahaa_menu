# Generated by Django 4.1.3 on 2022-11-29 07:31

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("website", "0011_video")]

    operations = [
        migrations.CreateModel(
            name="SocialMediaLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("facebook", models.CharField(blank=True, max_length=2000, null=True)),
                ("instagram", models.CharField(blank=True, max_length=2000, null=True)),
                ("whatsapp", models.CharField(blank=True, max_length=2000, null=True)),
                ("location", models.CharField(blank=True, max_length=2000, null=True)),
                ("resturant", models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="website.restaurant")),
            ],
        )
    ]
