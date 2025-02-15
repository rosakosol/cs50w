from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return f"{self.name}"

        
class Cuisine(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return f"{self.name}"


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
    
    def __str__(self):
        return f"{self.meal_type}"

    

class Recipe(models.Model):
    name = models.CharField(max_length=64, default="")
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient)
    description = models.TextField(default="")  
    image = models.ImageField(upload_to="images/%d/%m/%y", default=None)    
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name="recipes", null=True)
    
    
class CreateRecipeForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            "rows": 10,
            "cols": 80
        }))
    image_url = forms.ImageField()
    meal_type = forms.ModelChoiceField(
        queryset=MealType.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )
    cuisine = forms.ModelChoiceField(
        queryset=Cuisine.objects.all(),
        empty_label="Select a cuisine",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )