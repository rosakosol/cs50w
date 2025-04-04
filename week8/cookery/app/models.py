from django.db import models
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
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
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
    
        

class Tag(models.Model):
    name = models.CharField(max_length=64, default="")
    
    def __str__(self):
        return str(self.name)


class MealType(models.Model):
    name = models.CharField(max_length=64, default="")
    meal_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=64, default="", unique=True)
    cuisine = models.ManyToManyField(Cuisine, related_name="recipes")
    ratings = models.ManyToManyField(Rating, related_name="recipes", blank=True)
    ingredients = models.ManyToManyField(RecipeIngredient,  related_name="recipes")
    description = models.TextField()  
    instructions = models.TextField()
    servings = models.PositiveBigIntegerField(default=1)
    cook_time = models.PositiveBigIntegerField(default=0)
    prep_time = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to="images/%d/%m/%y", default="images/default-img.jpg")    
    image_alt_text = models.CharField(max_length=64, blank=True) 
    meal_type = models.ManyToManyField(MealType, related_name="recipes")
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
        ingredients = []
        
        # Get ingredients for the recipe
        for ri in self.ingredients.all():
            ingredients_schema = {
                    "@type": "HowToItem",
                    "name": ri.ingredient.name,
                    "quantity": {
                        "@type": "Quantity",
                        "value": ri.quantity,
                        "unitCode": ri.unit.name
                    }
            } 
            ingredients.append(ingredients_schema)
        
        return {
        "@context": "http://schema.org",
        "@type": "Recipe",
        "author": f"{self.user.first_name} {self.user.last_name}",
        "name": self.name,
        "recipeIngredient": ingredients,
        "description": self.description,
        "recipeInstructions": self.instructions, 
        "recipeYield": self.servings,
        "cookTime": f"PT{self.cook_time}M",
        "prepTime": f"PT{self.prep_time}M",
        "image": self.image.url if self.image else "",
        "dateCreated": f"{self.created_at}"
    }

    
    def __str__(self):
        return self.name
        
        
    

class Favourites(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="favourites")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favourites")
    added_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.recipe.name} in {self.favourites_list.name}"
    