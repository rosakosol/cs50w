from django.db import models
from django.contrib.auth.models import AbstractUser

BREAKFAST = 'BREAKFAST'
LUNCH = 'LUNCH'
DINNER = 'DINNER'

# Create your models here.
class Ingredient(models.Model):
    pass

class Recipe(models.Model):
    pass

class Cuisine(models.Model):
    pass

class Rating(models.Model):
    pass



class MealType(models.Model):
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