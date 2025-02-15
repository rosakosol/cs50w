from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Ingredient, Cuisine, Rating, MealType, Recipe, CreateRecipeForm



# Create your views here.
def index(request):
    user = request.user
    recipes = Recipe.objects.all().order_by("name")
    
    # If there are any recipes, paginate to 12 per page
    if recipes:
        paginator = Paginator(recipes, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # If no recipes, paginator is none
    else:
        page_obj = None
    
    
    return render(request, 'index.html', {
        "MEDIA_URL": settings.MEDIA_URL,
        "user": user,
        "recipes": recipes,
        "page_obj": page_obj,
    })


def add_recipe_view(request):
    user = request.user
    
    if user.is_authenticated:
        if request.method == "POST":
            
            # Create Listing Form
            create_form = CreateRecipeForm(request.POST)
            if create_form.is_valid():
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                image_url = form.cleaned_data.get('image_url', '')
                meal_type = form.cleaned_data['meal_type']
                cuisine = form.cleaned_data['cuisine']

                # Create a new Recipe instance
                recipe = Recipe.objects.create(
                    name=name,
                    description=description,
                    image_url=image_url,
                    meal_type=meal_type,
                    cuisine=cuisine,
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
    
