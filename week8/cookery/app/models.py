from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=64, default="")

        
class Cuisine(models.Model):
    name = models.CharField(max_length=64, default="")

class Rating(models.Model):
    value = models.IntegerField(default=1)
    
    def validate(self):
        if not 1 <= self.value <= 5:
            raiseValidationError("Rating must be between 1 and 5.")


class MealType(models.Model):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'

    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]
    
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_CHOICES,
        default=BREAKFAST,
    )
    

class Recipe(models.Model):
    name = models.CharField(max_length=64, default="")
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient)
    description = models.TextField(default="")  
    image_url = models.URLField(max_length=200, null=True, blank=True)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name="recipes", null=True)