from django.db import models
from django import forms
from django.forms import ModelForm, modelformset_factory
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Avg

# Create your models here.

# Standalone Ingredient
class Ingredient(models.Model):
    name = models.CharField(max_length=64, default="")
        
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return self.name

# Ingredients to be added to Recipe
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients", default="")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default="")
    quantity = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, default="")

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient} in {self.recipe}"

        
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
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return str(self.name)


class MealType(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=64, default="")
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True, related_name="recipes")
    ratings = models.ManyToManyField(Rating, related_name="recipes")
    ingredients = models.ManyToManyField(RecipeIngredient,  related_name="recipes")
    description = models.TextField(default="")  
    instructions = models.TextField(default="")
    servings = models.PositiveBigIntegerField(default=1)
    cook_time = models.PositiveBigIntegerField(default=0)
    prep_time = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="images/%d/%m/%y", default=None)    
    image_alt_text = models.CharField(max_length=64, blank=True) 
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name="recipes", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="recipes")
    
    schema = models.JSONField(blank=True, null=True)
    
    def get_ingredients(self):
        recipe_ingredients = self.recipe_ingredients.all()
        
        ingredient_names = []
        
        for recipe_ingredient in recipe_ingredients:
            ingredient_names.append(recipe_ingredient.ingredient.name)

        return ingredient_names
    
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
    
    def generate_schema(self):
        return {
        "@context": "http://schema.org",
        "@type": "Recipe",
        "author": f"{self.user.first_name} {self.user.last_name}",
        "name": self.name,
        "recipeCuisine": self.cuisine.name,
        # Ingredients
        "description": self.description,
        "recipeInstructions": self.instructions.split('\n'),  # assuming instructions are also stored this way
        "recipeYield": self.servings,
        "cookTime": f"PT{self.cook_time}M",
        "prepTime": f"PT{self.prep_time}M",
        "image": self.image.url if self.image else "",
        "dateCreated": f"{self.created_at}"
    }

    
    def __str__(self):
        return self.name
    
class CreateRecipeForm(forms.Form):
    name = forms.CharField(max_length=64)
    image = forms.ImageField(required=False)
    image_alt_text = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter alt text for image'}),
        required=False
    )
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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    servings = forms.IntegerField(
        min_value=1,
        max_value=99,
        required=True
    )
    cook_time = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True
    )
    prep_time = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True
    )
    
class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        required=True
    )    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True
    )
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=True
    )   
    
    
    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "quantity", "unit"]
        
RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=1)

    
class RecipeFilterForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tags"
    )
    cuisine = forms.ModelChoiceField(
        queryset=Cuisine.objects.all(),
        required=False,
        label="Cuisine",
        empty_label="Select a Cuisine"
    )
    meal_type = forms.ModelChoiceField(
        queryset=MealType.objects.all(),
        required=False,
        label="Meal Type",
        empty_label="Select a Meal Type"
    )
    

class Favourites(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="favourites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favourites")
    added_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.recipe.name} in {self.favourites_list.name}"
    
    
class FavouriteForm(forms.Form):
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[("add", "Add"), ("remove", "Remove")], widget=forms.HiddenInput())
    
