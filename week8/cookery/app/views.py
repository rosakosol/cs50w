from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import Ingredient, Unit, RecipeIngredient, Cuisine, Rating, RatingForm, MealType, Recipe, CreateRecipeForm, RecipeIngredientFormSet, Favourites, FavouriteForm, RecipeFilterForm
from django.db import IntegrityError
from django.utils import timezone
import json


# * Index Page
# Displays all recipes by default, paginated.
# Shows filter options
# TODO: Sort recipes from a-z; recently added; calorie count

def index(request):
    user = request.user
    recipes = Recipe.objects.all().order_by("-created_at")
    form_type = request.GET.get("form_type")
    
    # If user accessing filter form on index page
    if form_type == "filter":
        # Filter form 
        form = RecipeFilterForm(request.GET)

        # If the form is valid, filter the recipes
        if form.is_valid():
            # Dictionary for filters
            filter_data = {
                "tags__in": form.cleaned_data.get("tags"),
                "cuisine": form.cleaned_data.get("cuisine"),
                "meal_type": form.cleaned_data.get("meal_type")
            }
            
            # Loop through filtered data and return recipes
            for field, value in filter_data.items():
                if value:
                    recipes = recipes.filter(**{field: value})
        
    # Else if user is filtering from backlinked recipe buttons        
    else:
        # If user has passed through a filter to index page - i.e. from clicking a tag button on recipe page
        filter_data = {
            "tags__name": request.GET.get("tags"),
            "cuisine__name": request.GET.get("cuisine"),
            "meal_type__name": request.GET.get("meal_type")
        }
        
        # Loop through filtered data and return recipes
        for field, value in filter_data.items():
            if value:
                recipes = recipes.filter(**{field: value})
    
    # Display empty filter form  
    form = RecipeFilterForm()

    
    # If there are any recipes, paginate
    if recipes:
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        
    else:
        page_obj = None
    
    return render(request, "index.html", {
        "MEDIA_URL": settings.MEDIA_URL,
        "user": user,
        "form": form,
        "recipes": recipes,
        "page_obj": page_obj
    })
    
    
    
    
# * Recipe Page
# Displays single recipe in detail including description, ingredients and instructions
# Shows filter buttons for each recipe
# Allows logged-in users to submit ratings and add recipe to favourites
# If user is author, they can edit and delete recipes
# Buttons: Share via email, socials, and print-friendly version  

def recipe(request, recipe_name):
    user = request.user
    recipe = get_object_or_404(Recipe, name=recipe_name)
    tags = recipe.tags.all()
    
    # If user is logged-in, they can rate and favourite recipes
    if user.is_authenticated:
        # Differentiate between rating and favourite forms
        form_type = request.POST.get("form_type")
        
        # Check if there is an existing rating
        existing_rating = Rating.objects.filter(user=user, recipe=recipe).first()
        
        # If rating form has been submitted
        if form_type == "rating":
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                # Check if user has rated before
                if existing_rating:
                    existing_rating.value = rating_form.cleaned_data["value"]
                    existing_rating.save()
                    messages.success(request, "Your rating has been saved successfully!")

                else:
                    rating = Rating()
                    rating.value = rating_form.cleaned_data["value"]
                    rating.user = user
                    rating.recipe = recipe
                    rating.save()
                    recipe.ratings.add(rating)
                    messages.success(request, "Your rating has been placed successfully!")
                
                # Refresh recipe in db
                recipe.refresh_from_db()
                return HttpResponseRedirect(reverse("recipe", args=[recipe_name]))
            
        else:
            favourite_form = FavouriteForm(request.POST)
            if favourite_form.is_valid():
                action = favourite_form.cleaned_data["action"]
                
                if action == "add":
                    if not Favourites.objects.filter(user=user, recipe=recipe).exists():
                        Favourites.objects.create(user=user, recipe=recipe)
                        
                elif action == "remove":
                    favourite_instance = Favourites.objects.filter(user=user, recipe=recipe).first()
                    if favourite_instance:
                        favourite_instance.delete()


                recipe.refresh_from_db()
                return HttpResponseRedirect(reverse("recipe", args=[recipe_name]))
                    
        # If user is logged in but has not submitted any forms, display empty forms
        rating_form = RatingForm()
        favourite_form = FavouriteForm()
        is_favourited = Favourites.objects.filter(user=request.user, recipe=recipe).exists()

    else:
        existing_rating = None
        rating_form = None
        favourite_form = None
        is_favourited = False
    
    return render(request, "recipe.html", {
        "user": user,
        "recipe": recipe,
        "tags": tags,
        "rating_form": rating_form,
        "favourite_form": favourite_form,
        "is_favourited": is_favourited,
        "existing_rating": existing_rating
    })


def add_recipe_view(request):
    user = request.user
    
    if user.is_authenticated:
        if request.method == "POST":
            
            # Create Listing Form
            create_form = CreateRecipeForm(request.POST, request.FILES)
            formset = RecipeIngredientFormSet(request.POST)
            
            if create_form.is_valid() and formset.is_valid():
                
                name = create_form.cleaned_data["name"]
                cuisine = create_form.cleaned_data["cuisine"]
                description = create_form.cleaned_data["description"]
                instructions = create_form.cleaned_data["instructions"]
                servings = create_form.cleaned_data["servings"]
                cook_time = create_form.cleaned_data["cook_time"]
                prep_time = create_form.cleaned_data["prep_time"]
                image = create_form.cleaned_data["image"]
                image_alt_text = create_form.cleaned_data["image_alt_text"]
                meal_type = create_form.cleaned_data["meal_type"]
                tags = create_form.cleaned_data["tags"]

                # Create a new Recipe instance
                recipe = Recipe.objects.create(
                    user=user,
                    name=name,
                    cuisine=cuisine,
                    description=description,
                    instructions=instructions,
                    servings=servings,
                    cook_time=cook_time,
                    prep_time=prep_time,
                    image=image,
                    image_alt_text=image_alt_text,
                    meal_type=meal_type,
                )           
                
                schema = recipe.generate_schema()
                recipe.schema = schema
                recipe.tags.set(tags)
                recipe.save()
                
                for form in formset:
                    ingredient = form.cleaned_data.get("ingredient")
                    quantity = form.cleaned_data.get("quantity")
                    unit = form.cleaned_data.get("unit")
                    if ingredient and quantity:
                        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity, unit=unit)
                
                # Redirect to the same page to show the new
                return HttpResponseRedirect(reverse("index"))  
        
            
            # Check for AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
                
                try:
                    formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
                    new_form = formset.empty_form
                    html = render_to_string("ingredient_form_partial.html", {
                        "form": new_form
                    })
                    
                    
                    return JsonResponse({
                        "html": html
                    }) 
                except json.JSONDecodeError:
                    return JsonResponse({
                        "error": "Invalid JSON data"
                    }, status=400)

        
        else:
            create_form = CreateRecipeForm()
            formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
        
        return render(request, "add_recipe.html", {
            "user": user,
            "create_form": create_form,
            "formset": formset
        })
    else:
        return render(request, "access_denied.html")

    
    
@login_required
def edit_recipe(request, recipe_id):
    user = request.user
    
    # Get the recipe object if it exists
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    # Ensure the logged-in user is the author of the recipe
    if recipe.user != user:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            new_name = data.get('name', recipe.name)  # Default to current name if not provided
            new_description = data.get('description', recipe.description)  # Default to current description if not provided
            new_instructions = data.get('instructions', recipe.instructions)  # Default to current instructions if not provided
            
            # Update the recipe fields
            recipe.name = new_name
            recipe.description = new_description
            recipe.instructions = new_instructions 
            
            # Save the updated recipe
            recipe.save()
            
            # Return a JSON response with success and updated data
            return JsonResponse({
                "success": True,
                "updated_name": recipe.name,
                "updated_description": recipe.description,
                "updated_instructions": recipe.instructions
            })
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)
    return JsonResponse({
        "error": "Invalid request."
    }, status=400)
    
    
@login_required
def delete_recipe(request, recipe_id):
    user = request.user
    
    # Get the recipe object if it exists
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    # Ensure the logged-in user is the author of the recipe
    if recipe.user != user:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        # Delete the recipe
        recipe.delete()

        return JsonResponse({
            "success": True,
            "message": "Recipe deleted successfully."
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def favourites_view(request):
    user = request.user
    
    if user.is_authenticated:
        # Display favourites
        favourites = Recipe.objects.filter(favourites__user=user)
    else:
        favourites = []

    # If there are any recipes, paginate
    if favourites:
        paginator = Paginator(favourites, 6)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        
    # If no recipes, paginator is none
    else:
        page_obj = None
        
        
    return render(request, "favourites.html", {
        "user": user,
        "favourites": favourites,
        "page_obj": page_obj
    })
    
    
    
def search(request):
    user = request.user
    query = request.POST.get("q")
    recipes = Recipe.objects.all()
    
    # If query read
    if query:
        results = []
        
        # If search query substring in recipe name then add to list of search results
        for recipe in recipes:
            if query.lower() in recipe.name.lower():
                results.append(recipe)
        
        # If there are any recipes, paginate
        if results:
            paginator = Paginator(results, 6)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)
            
            # If no recipes, paginator is none and return no results page
        else:
            page_obj = None
            return render(request, 'no_results.html')
            
        # Else render index page with search results
        return render(request, 'index.html', {
            "MEDIA_URL": settings.MEDIA_URL,
            "user": user,
            "recipes": results,
            "page_obj": page_obj
        })
    # If query cannot be read, display error message
    else:     
        messages.error("Query could not be read!")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
