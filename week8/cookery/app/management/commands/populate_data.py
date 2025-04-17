import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import Recipe, Cuisine, Tag, Unit, Ingredient, RecipeIngredient, MealType


class Command(BaseCommand):
    help = 'Populates initial Ingredients, Cuisines, Mealtypes, Units and Tags'

    def handle(self, *args, **kwargs):
        ingredients = [
            "Sugar", "Salt", "Butter", "Olive Oil", "Eggs", "Flour", "Garlic", "Onions", "Milk", "Cheese",
            "Chicken", "Tomatoes", "Potatoes", "Rice", "Pasta", "Lemon", "Carrots", "Bacon", "Spinach", "Cucumber",
            "Mushrooms", "Cilantro", "Pepper", "Parsley", "Ground Beef", "Cabbage", "Zucchini", "Basil", "Thyme", "Oregano",
            "Chili Powder", "Paprika", "Cinnamon", "Rosemary", "Ginger", "Coconut Milk", "Peas", "Bell Peppers", "Avocados", "Soy Sauce",
            "Yogurt", "Tomato Paste", "Tuna", "Almonds", "Walnuts", "Chickpeas", "Lentils", "Green Beans", "Corn", "Apples",
            "Cauliflower", "Broccoli", "Raisins", "Maple Syrup", "Vanilla Extract", "Honey", "Peanut Butter", "Sesame Oil", "Mustard", "Ketchup",
            "Pineapple", "Mango", "Beef", "Pork", "Shrimp", "Clams", "Scallops", "Salmon", "Tamarind", "Wasabi",
            "Noodles", "Bread", "Pita", "Quinoa", "Couscous", "Feta Cheese", "Parmesan", "Mozzarella", "Blue Cheese", "Heavy Cream",
            "Oats", "Chia Seeds", "Flax Seeds", "Sunflower Seeds", "Pumpkin Seeds", "Hazelnuts", "Pecans", "Macadamia Nuts", "Cashews", "Prawns",
            "Anchovies", "Capers", "Artichokes", "Leeks", "Radishes", "Celery", "Endive", "Kale", "Swiss Chard", "Turnips",
            "Sweet Potatoes", "Butternut Squash", "Acorn Squash", "Brussels Sprouts", "Eggplant", "Okra", "Watermelon", "Cantaloupe", "Peaches", "Plums",
            "Cherries", "Grapes", "Strawberries", "Blueberries", "Raspberries", "Blackberries", "Kiwi", "Lychee", "Passionfruit", "Dragonfruit",
            "Guava", "Fig", "Dates", "Goji Berries", "Seaweed", "Tofu", "Tempeh", "Seitan", "Miso Paste", "Kimchi",
            "Sauerkraut", "Pickles", "Relish", "Molasses", "Brown Sugar", "Icing Sugar", "Glucose Syrup", "Cornstarch", "Arrowroot Powder", "Baking Soda",
            "Baking Powder", "Yeast", "Gelatin", "Agar Agar", "Tapioca Pearls", "Rice Vinegar", "Balsamic Vinegar", "White Vinegar", "Apple Cider Vinegar", "Red Wine Vinegar",
            "Sriracha", "Tabasco", "Chili Flakes", "Curry Powder", "Turmeric", "Cumin", "Coriander", "Fenugreek", "Star Anise", "Cardamom",
            "Cloves", "Nutmeg", "Allspice", "Sumac", "Za'atar", "Harissa", "Berbere", "Dukkah", "Herbes de Provence", "Italian Seasoning",
            "Garam Masala", "Cajun Spice", "Old Bay", "Poultry Seasoning", "Steak Seasoning", "Lemon Pepper", "Onion Powder", "Garlic Powder", "Celery Salt", "Smoked Paprika",
            "White Pepper", "Black Peppercorns", "Green Peppercorns", "Pink Peppercorns", "Juniper Berries", "Dill", "Sage", "Marjoram", "Lovage", "Bay Leaves"
        ]

        cuisines = [
            "Italian", "Chinese", "Indian", "Mexican", "French", "Japanese", "Mediterranean"
        ]

        meal_types = [
            ("Breakfast", 1),
            ("Lunch", 2),
            ("Dinner", 3),
            ("Snack", 4),
            ("Dessert", 5)
        ]
        
        units = [
            "grams", "kilograms", "milliliters", "liters", "cup", "tablespoon", "teaspoon", "piece", "pinch", "dash"
        ]
        
        tags = [
            "High-Protein", "Low-Carb", "Healthy", "Vegetarian", "Vegan", "Quick", "Gluten-Free"
        ]


        for name in ingredients:
            obj, created = Ingredient.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Ingredient: {name}"))

        for name in cuisines:
            obj, created = Cuisine.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Cuisine: {name}"))

        for name, order in meal_types:
            obj, created = MealType.objects.get_or_create(name=name, meal_order=order)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added MealType: {name}"))
                
        for name in units:
            obj, created = Unit.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Unit: {name}"))
                
        for name in tags:
            obj, created = Tag.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added Tag: {name}"))

        self.stdout.write(self.style.SUCCESS("Populated Ingredients, Cuisines, MealTypes, Units and Tags"))
