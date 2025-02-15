# Generated by Django 5.1.6 on 2025-02-15 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_recipe_image_url_recipe_meal_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image_url',
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, upload_to='images/%d/%m/%y'),
        ),
    ]
