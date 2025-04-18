from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import Ingredient, Unit, Tag, RecipeIngredient, Cuisine, Rating, MealType, Recipe, Favourites
from .forms import RatingForm, CreateRecipeForm, RecipeIngredientFormSet, FavouriteForm, RecipeFilterForm, SortForm
from django.db import IntegrityError
from django.utils import timezone
import json



# * Index
# Displays all recipes by default, paginated.
# Shows filter options and sort recipes
def index(request):
    user = request.user
    all_meal_types = MealType.objects.all()
    all_cuisines = Cuisine.objects.all().order_by("name")
    all_tags = Tag.objects.all().order_by("name")
    recipes = Recipe.objects.all().order_by("-created_at")
    form_type = request.GET.get("form_type")
    sort_form = SortForm(request.GET)
 
    
    # If user accessing filter form on index page
    if form_type == "filter":
        # Filter form 
        filter_form = RecipeFilterForm(request.GET)

        # If the form is valid, filter the recipes
        if filter_form.is_valid():
            # Dictionary for filters
            filter_data = {
                "tags__in": filter_form.cleaned_data.get("tags"),
                "cuisine__in": filter_form.cleaned_data.get("cuisine"),
                "meal_type__in": filter_form.cleaned_data.get("meal_type")
            }
            
            # Loop through filtered data and return recipes
            for field, value in filter_data.items():
                if value:
                    recipes = recipes.filter(**{field: value})
                    
            # Make sure the result is distinct with no dupe recipes
            recipes = recipes.distinct()
        
    # Else if user is filtering from backlinked recipe buttons        
    else:
        filter_form = RecipeFilterForm()
        
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

    
    if sort_form.is_valid():
        sort_by = sort_form.cleaned_data.get("sort_by")
        if sort_by == "name_asc":
            recipes = recipes.order_by("name")
        elif sort_by == "name_desc":
            recipes = recipes.order_by("-name")
        elif sort_by == "oldest":
            recipes = recipes.order_by("created_at")
        elif sort_by == "newest":
            recipes = recipes.order_by("-created_at")

    
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
        "filter_form": filter_form,
        "sort_form": sort_form,
        "recipes": recipes,
        "page_obj": page_obj,
        "all_cuisines": all_cuisines,
        "all_tags": all_tags,
        "all_meal_types": all_meal_types
    })
    
    
    
    
# * Recipe
# Displays single recipe in detail including description, ingredients and instructions
# Shows filter buttons for each recipe
# Allows logged-in users to submit ratings and add recipe to favourites
# If user is author, they can edit and delete recipes
# Buttons: Share via email, socials, and print-friendly version  
def recipe(request, recipe_name):
    user = request.user
    all_meal_types = MealType.objects.all()
    all_cuisines = Cuisine.objects.all().order_by("name")
    all_tags = Tag.objects.all().order_by("name")
    recipe = get_object_or_404(Recipe, name=recipe_name)
    
    # If user is logged-in, they can rate and favourite recipes
    if user.is_authenticated:
        # Differentiate between rating and favourite forms
        form_type = request.POST.get("form_type")
        
        # If rating form has been submitted
        if form_type == "rating":
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                # Check if user has rated before
                existing_rating = Rating.objects.filter(user=user, recipe=recipe).first()
        
                if existing_rating:
                    existing_rating.value = rating_form.cleaned_data["value"]
                    existing_rating.save()
                    messages.success(request, "Your rating has been saved successfully!")

                else:
                    rating = rating_form.save(commit=False)
                    rating.user = user
                    rating.recipe = recipe
                    rating.save()
                    recipe.ratings.add(rating)
                    messages.success(request, "Your rating has been placed successfully!")
                
                return HttpResponseRedirect(reverse("recipe", args=[recipe_name]))
            
        else:
            favourite_form = FavouriteForm(request.POST)
            if favourite_form.is_valid():
                action = favourite_form.cleaned_data["action"]
                
                if action == "add":
                    if not Favourites.objects.filter(user=user, recipe=recipe).exists():
                        Favourites.objects.create(user=user, recipe=recipe)
                        messages.success(request, "Recipe has been added to favourites!")
                        
                elif action == "remove":
                    favourite_instance = Favourites.objects.filter(user=user, recipe=recipe).first()
                    if favourite_instance:
                        favourite_instance.delete()
                        messages.error(request, "Recipe removed from favourites.")

                return HttpResponseRedirect(reverse("recipe", args=[recipe_name]))
                    
        # If user is logged in but has not submitted any forms, display empty forms
        rating_form = RatingForm()
        favourite_form = FavouriteForm()
        is_favourited = Favourites.objects.filter(user=request.user, recipe=recipe).exists()
        existing_rating = None

    # Else if user is not logged in
    else:
        existing_rating = None
        rating_form = None
        favourite_form = None
        is_favourited = False
    
    return render(request, "recipe.html", {
        "user": user,
        "recipe": recipe,
        "rating_form": rating_form,
        "favourite_form": favourite_form,
        "is_favourited": is_favourited,
        "existing_rating": existing_rating,
        "all_cuisines": all_cuisines,
        "all_tags": all_tags,
        "all_meal_types": all_meal_types
    })



# * Add Recipe
# Displays add recipe form
def add_recipe_view(request):
    user = request.user
    all_meal_types = MealType.objects.all()
    all_cuisines = Cuisine.objects.all().order_by("name")
    all_tags = Tag.objects.all().order_by("name")
    
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
                    description=description,
                    instructions=instructions,
                    servings=servings,
                    cook_time=cook_time,
                    prep_time=prep_time,
                    image=image,
                    image_alt_text=image_alt_text,
                )        
                
                schema = recipe.generate_schema()
                recipe.schema = schema
                
                recipe.tags.set(tags)
                recipe.cuisine.set(cuisine)
                recipe.meal_type.set(meal_type)
                
                recipe.save()
                
                for form in formset:
                    ingredient = form.cleaned_data.get("ingredient")
                    quantity = form.cleaned_data.get("quantity")
                    unit = form.cleaned_data.get("unit")

                    if ingredient and quantity:
                        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity, unit=unit)

                
                # Redirect to newly created recipe page
                return HttpResponseRedirect(reverse("recipe", args=[recipe.name])) 

        
        else:
            create_form = CreateRecipeForm()
            formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.none())
        
        return render(request, "add_recipe.html", {
            "user": user,
            "create_form": create_form,
            "formset": formset,
            "all_cuisines": all_cuisines,
            "all_tags": all_tags,
            "all_meal_types": all_meal_types
        })
    else:
        return render(request, "access_denied.html")

    
    
    
# * Edit recipe
# Allow users to edit recipe name, description and instructions dynamically
@login_required
def edit_recipe(request, recipe_id):    
    if request.method == "POST":
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        
        # If user is not the author, display unauthorised error
        if recipe.user != user:
            return JsonResponse({"error": "Unauthorised"}, status=403)
    
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            new_name = data.get("name", recipe.name)
            new_description = data.get("description", recipe.description)
            new_instructions = data.get("instructions", recipe.instructions)  # Default to current instructions if not provided
            
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
                "updated_instructions": recipe.instructions,
            })
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)
        
    return JsonResponse({
        "error": "Invalid request."
    }, status=400)
    
    
    
    
    
# * Delete recipe
# Allow users to delete recipe
@login_required
def delete_recipe(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    # If user is not author, display unauthorised error
    if recipe.user != user:
        return JsonResponse({"error": "Unauthorised"}, status=403)
    
    try:
        recipe.delete()

        return JsonResponse({
            "success": True,
            "message": "Recipe deleted successfully."
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




# * Favourites
# Display favourited recipes
def favourites_view(request):
    user = request.user
    all_meal_types = MealType.objects.all()
    all_cuisines = Cuisine.objects.all().order_by("name")
    all_tags = Tag.objects.all().order_by("name")
    form_type = request.GET.get("form_type")
    sort_form = SortForm(request.GET)
 
    
    if user.is_authenticated:
        recipes = Recipe.objects.filter(favourites__user=user)
        
        # If user accessing filter form 
        if form_type == "filter":
            # Filter form 
            filter_form = RecipeFilterForm(request.GET)

            # If the form is valid, filter the recipes
            if filter_form.is_valid():
                # Dictionary for filters
                filter_data = {
                    "tags__in": filter_form.cleaned_data.get("tags"),
                    "cuisine__in": filter_form.cleaned_data.get("cuisine"),
                    "meal_type__in": filter_form.cleaned_data.get("meal_type")
                }
                
                # Loop through filtered data and return recipes
                for field, value in filter_data.items():
                    if value:
                        recipes = recipes.filter(**{field: value})
                        
                # Make sure the result is distinct with no dupe recipes
                recipes = recipes.distinct()
                
        else:
            filter_form = RecipeFilterForm()

        
        if sort_form.is_valid():
            sort_by = sort_form.cleaned_data.get("sort_by")
            if sort_by == "name_asc":
                recipes = recipes.order_by("name")
            elif sort_by == "name_desc":
                recipes = recipes.order_by("-name")
            elif sort_by == "oldest":
                recipes = recipes.order_by("created_at")
            elif sort_by == "newest":
                recipes = recipes.order_by("-created_at")

        # If there are any recipes, paginate
        if recipes:
            paginator = Paginator(recipes, 6)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)
            
        # If no recipes, paginator is none
        else:
            recipes = []
            page_obj = None      
        
        return render(request, "favourites.html", {
            "user": user,
            "recipes": recipes,
            "filter_form": filter_form,
            "sort_form": sort_form,
            "page_obj": page_obj,
            "all_cuisines": all_cuisines,
            "all_tags": all_tags,
            "all_meal_types": all_meal_types
        })
    
    else:
        return render(request, "access_denied.html", {
            "all_cuisines": all_cuisines,
            "all_tags": all_tags,
            "all_meal_types": all_meal_types,
        })
       
        
    

# * Sort
# Sort recipes on index page
def sort(request):
    user = request.user
    all_meal_types = MealType.objects.all()
    all_cuisines = Cuisine.objects.all().order_by("name")
    all_tags = Tag.objects.all().order_by("name")
    filter_form = RecipeFilterForm()
    sort_by = request.GET.get("sort_by", "")  # Default sorting
    
    if sort_by == "name_asc":
        recipes = Recipe.objects.all().order_by("name")
    elif sort_by == "name_desc":
        recipes = Recipe.objects.all().order_by("-name")
    elif sort_by == "oldest":
        recipes = Recipe.objects.all().order_by("created_at")
    elif sort_by == "newest":
        recipes = Recipe.objects.all().order_by("-created_at")
        
    # If there are any recipes, paginate
    if recipes:
        paginator = Paginator(recipes, 6)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        
        # If no recipes, paginator is none and return no results page
    else:
        page_obj = None
        return render(request, "no_results.html", {
            "all_cuisines": all_cuisines,
            "all_tags": all_tags,
            "all_meal_types": all_meal_types
        })
        
    # Else render index page with search results
    return render(request, "index.html", {
        "MEDIA_URL": settings.MEDIA_URL,
        "user": user,
        "filter_form": filter_form,
        "recipes": recipes,
        "page_obj": page_obj
    })




# * Search function
# Return search results for query
def search(request):
    user = request.user
    all_meal_types = MealType.objects.all()
    all_cuisines = Cuisine.objects.all().order_by("name")
    all_tags = Tag.objects.all().order_by("name")
    recipes = Recipe.objects.all()
    
    # Get query from search form
    query = request.GET.get("q", "").strip()

    if query:
        results = Recipe.objects.filter(name__icontains=query)
        
        # If there are any recipes, paginate
        if results:
            paginator = Paginator(results, 6)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)
            
            # If no recipes, paginator is none and return no results page
        else:
            page_obj = None
            return render(request, "no_results.html", {
                "all_cuisines": all_cuisines,
                "all_tags": all_tags,
                "all_meal_types": all_meal_types 
            })
            
        # Else render index page with search results
        return render(request, "search.html", {
            "MEDIA_URL": settings.MEDIA_URL,
            "user": user,
            "query": query,
            "recipes": recipes,
            "page_obj": page_obj,
            "all_cuisines": all_cuisines,
            "all_tags": all_tags,
            "all_meal_types": all_meal_types
        })
    # If query cannot be read, redirect to index
    else:     
        return HttpResponseRedirect(reverse("index"))




# * Login
# Allow users to login via username and password
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




# * Logout
# Allow users to logout and redirect to index
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))




# * Register
# Allow users to register
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
    
