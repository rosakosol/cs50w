# Generated by Django 5.1.4 on 2025-01-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]