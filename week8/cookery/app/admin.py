from django.contrib import admin

# Register your models here.
from .models import Ingredient, Cuisine, MealType, Recipe

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)

class CuisineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ("meal_type",)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "cuisine", "meal_type")
    ordering = ("name",)
    
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(MealType, MealTypeAdmin)
admin.site.register(Recipe, RecipeAdmin)
    