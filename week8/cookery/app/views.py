from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import Ingredient, RecipeIngredient, Cuisine, Rating, RatingForm, MealType, Recipe, CreateRecipeForm, RecipeIngredientFormSet, Favourites, FavouriteForm, RecipeFilterForm
from django.db import IntegrityError
from django.utils import timezone
import json



# Create your views here.
def index(request):
    user = request.user
    recipes = Recipe.objects.all().order_by("-created_at")
    
    # Filter form 
    form = RecipeFilterForm(request.GET)

    # If the form is valid, filter the recipes
    if form.is_valid():
        # Get filter data from the form
        tags = form.cleaned_data["tags"]
        cuisine = form.cleaned_data["cuisine"]
        meal_type = form.cleaned_data["meal_type"]

        # Filter by tags (only if tags are selected)
        if tags:
            recipes = recipes.filter(tags__in=tags)

        # Filter by cuisine (only if cuisine is selected)
        if cuisine:
            recipes = recipes.filter(cuisine=cuisine)

        # Filter by meal type (only if meal type is selected)
        if meal_type:
            recipes = recipes.filter(meal_type=meal_type)
    
    # If user has passed through a filter to index page - i.e. from clicking a tag button on recipe page
    tag_name = request.GET.get("tag")
    cuisine_name = request.GET.get("cuisine")
    meal_type_name = request.GET.get("meal_type")
    
    if tag_name:
        recipes = recipes.filter(tags__name=tag_name)
        
    if cuisine_name:
        recipes = recipes.filter(cuisine__name=cuisine_name)
        
    if meal_type_name:
        recipes = recipes.filter(meal_type__name=meal_type_name)

    
    # If there are any recipes, paginate
    if recipes:
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        
        # If no recipes, paginator is none
    else:
        page_obj = None
    
    return render(request, 'index.html', {
        "MEDIA_URL": settings.MEDIA_URL,
        "user": user,
        "form": form,
        "recipes": recipes,
        "page_obj": page_obj
    })
    
def recipe(request, recipe_name):
    user = request.user
    recipe = get_object_or_404(Recipe, name=recipe_name)
    tags = recipe.tags.all()
    
    if user.is_authenticated:
        existing_rating = Rating.objects.filter(user=user, recipe=recipe).first()

        if request.method == "POST":
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
            
        
            favourite_form = FavouriteForm(request.POST)
            if favourite_form.is_valid():
                action = favourite_form.cleaned_data["action"]
                
                if action == "add":
                    # Check if user has already favourited recipe
                    if not Favourites.objects.filter(user=user, recipe=recipe).exists():
                        Favourites.objects.create(user=user, recipe=recipe)
                        
                elif action == "remove":
                    favourite_instance = Favourites.objects.filter(user=user, recipe=recipe).first()
                    if favourite_instance:
                        favourite_instance.delete()


                recipe.refresh_from_db()
                return HttpResponseRedirect(reverse("recipe", args=[recipe_name]))
                    
        # If user is logged in, display empty form 
        else:
            rating_form = RatingForm()
            favourite_form = FavouriteForm()

        is_favourited = Favourites.objects.filter(user=request.user, recipe=recipe).exists()

    else:
        existing_rating = None
        rating_form = None
        favourite_form = None
        is_favourited = False
        
    print(recipe.schema)
    
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
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)
                
                # Redirect to the same page to show the new comment
                return HttpResponseRedirect(reverse("index"))  
        
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
    
