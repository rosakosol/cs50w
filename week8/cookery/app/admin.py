from django.contrib import admin

# Register your models here.
from .models import Ingredient, RecipeIngredient, Cuisine, MealType, Recipe, Rating, Tag

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("ingredient",)
    ordering = ("ingredient",)

class CuisineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    
class MealTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ["meal_order",]
    

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "average_rating")
    ordering = ("name",)
    filter_horizontal = ("ratings",)
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ("value",)
    ordering = ("value",)
    
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)

    
    
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(MealType, MealTypeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Tag, TagAdmin)