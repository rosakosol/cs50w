from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import Ingredient, Cuisine, Rating, RatingForm, MealType, Recipe, CreateRecipeForm
from django.db import IntegrityError



# Create your views here.
def index(request):
    user = request.user
    recipes = Recipe.objects.all().order_by("-created_at")
    
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
        "recipes": recipes,
        "page_obj": page_obj
    })
    
def recipe(request, recipe_name):
    user = request.user
    recipe = get_object_or_404(Recipe, name=recipe_name)
    
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
                    existing_rating = None
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
            rating_form = RatingForm()
    else:
        existing_rating = None
        rating_form = None
    
    return render(request, "recipe.html", {
        "user": user,
        "recipe": recipe,
        "rating_form": rating_form,
        "existing_rating": existing_rating
    })


def add_recipe_view(request):
    user = request.user
    
    if user.is_authenticated:
        if request.method == "POST":
            
            # Create Listing Form
            create_form = CreateRecipeForm(request.POST, request.FILES)
            if create_form.is_valid():

                name = create_form.cleaned_data["name"]
                description = create_form.cleaned_data["description"]
                image = create_form.cleaned_data["image"]
                meal_type = create_form.cleaned_data["meal_type"]
                cuisine = create_form.cleaned_data["cuisine"]
                instructions = create_form.cleaned_data["instructions"]
                ingredients = create_form.cleaned_data["ingredients"]

                # Create a new Recipe instance
                recipe = Recipe.objects.create(
                    name=name,
                    description=description,
                    image=image,
                    meal_type=meal_type,
                    cuisine=cuisine,
                    instructions=instructions,
                    ingredients=ingredients
                )           
                # Redirect to the same page to show the new comment
                return HttpResponseRedirect(reverse("index"))  
        
        else:
            create_form = CreateRecipeForm()
        
        return render(request, "add_recipe.html", {
            "user": user,
            "create_form": create_form,
        })
    else:
        return render(request, "access_denied.html")

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
    
