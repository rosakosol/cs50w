from django.contrib import admin

# Register your models here.
from .models import Ingredient, Cuisine, MealType, Recipe, Rating, Tag

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)

class CuisineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "cuisine", "average_rating")
    ordering = ("name",)
    filter_horizontal = ("ratings",)
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ("value",)
    ordering = ("value",)
    
class TagAdmin(admin.ModelAdmin):
    list_display = ("value",)
    ordering = ("value",)

    
    
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(MealType, MealTypeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Tag, TagAdmin)