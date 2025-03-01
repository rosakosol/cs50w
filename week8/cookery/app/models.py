from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Avg

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=64, default="")
    calories_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    unit = models.CharField(max_length=64, default="", blank=True)
    
    
    def __str__(self):
        return self.name
        
class Cuisine(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default="")
    value = models.IntegerField(default=1)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, default="", null=True)
    
    def clean(self):
        if not 1 <= self.value <= 5:
            raise ValidationError("Rating must be between 1 and 5.")
            
    def __str__(self):
        return str(self.value)
            
class RatingForm(forms.Form):
    value = forms.ChoiceField(
        choices=[(str(i), i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )

class Tag(models.Model):
    value = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return str(self.value)


class MealType(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=64, default="")
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    ratings = models.ManyToManyField(Rating, related_name="recipes")
    ingredients = models.ManyToManyField(Ingredient,  related_name="recipes")
    description = models.TextField(default="")  
    instructions = models.TextField(default="")
    servings = models.PositiveBigIntegerField(default=1)
    cooking_time = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="images/%d/%m/%y", default=None)    
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name="recipes", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="recipes")
    
    def average_rating(self):
        average = self.ratings.aggregate(Avg('value'))['value__avg']
        return average if average is not None else 0
    
    def total_calories(self):
        total_calories = 0
        for recipe_ingredient in self.recipe_ingredients.all():
            ingredient_calories = recipe_ingredient.ingredient.calories_per_unit * recipe_ingredient.quantity
            total_calories += ingredient_calories
        return total_calories
    
    def total_calories_per_serving(self):
        return self.total_calories() / self.servings

    
    def __str__(self):
        return self.name
    
class CreateRecipeForm(forms.Form):
    name = forms.CharField(max_length=64)
    image = forms.ImageField(required=False)
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
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            "rows": 10,
            "cols": 80
        }))
    instructions = forms.CharField(
        label="Instructions",
        widget=forms.Textarea(attrs={
            "rows": 10,
            "cols": 80
        }))
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class Favourites(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="favourites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favourites")
    added_at = models.DateTimeField(auto_now_add=True) 
    
    
class FavouriteForm(forms.Form):
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[("add", "Add"), ("remove", "Remove")], widget=forms.HiddenInput())