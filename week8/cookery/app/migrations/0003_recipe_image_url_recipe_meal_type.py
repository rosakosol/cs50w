# Generated by Django 5.1.6 on 2025-02-15 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cuisine_name_ingredient_name_rating_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='meal_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='app.mealtype'),
        ),
    ]
