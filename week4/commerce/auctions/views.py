from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Listing, Category, Bid, Comment


# Display active listings when user is logged in
def index(request):
    # Get the current logged-in user
    user = request.user
    listings = Listing.objects.all()
    
    return render(request, "auctions/index.html", {
        "user": user,
        "listings": listings
    })
        

# Create a new listing
def create_listing(request):
    pass


def create_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    highest_bid = listing.current_highest_bid()
    
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save()
            if bid.current > highest_bid and bid.current >= listing.starting_bid:
                bid.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Your bid must be higher than the current bid.")

# Display listing page
def listing_page(request, listing_id):
    # Get the current logged-in user
    user = request.user
    
    # Get listing by unique id
    listing = Listing.objects.get(pk=listing_id)
    category = listing.category
    comments = listing.comments.all()
    
    # Pagination for comments
    paginator = Paginator(comments, 10)  # Show 10 comments per page
    page_number = request.GET.get('page')  # Get the page number from the URL query string
    page_obj = paginator.get_page(page_number)  # Get the page of comments
    
    # If user is logged in:
        # User can add item to watchlist
        
        # If item is already on watchlist, clicking the button will remove it from watchlist
        
        # If user is creator of listing, they can close the auction which makes highest bidder the winner of the auction and renders the listing inactive
        
        # If user is signed in on a inactive listing page, and user is the winning bidder, page should display message that indicates so
        
        # User can add comments to listing page
    

    
    return render(request, "auctions/listing.html", {
        "user": user,
        "listing": listing,
        "category": category,
        "comments": comments,
        "page_obj": page_obj
    })
        
# Display a list of all listing categories, clicking on name of category should take user to page with all active listings under category
def categories(request):
    user = request.user
    listings = Listing.objects.all()
    categories = Category.objects.all()
    
    return render(request, "auctions/categories.html", {
        "user": user,
        "listings": listings,
        "categories": categories
    })

# Display all active listings for a given category
def category_listings(request, category_name):
    user = request.user

    # Get category by name
    category = Category.objects.get(name=category_name)
     
    # Fetch active listings for the category
    if category:
        listings = category.listings.filter(is_active=True)

    # Pass the listings to the template
    return render(request, "auctions/category_listings.html", {
        "listings": listings,
        "category": category
    })


# Watchlist where logged in users can see their saved items, clicking on any listing should take them to listing page
def watchlist(request):
    pass


# If user is logged in, they can create a new listing
    # Title
    # Description
    # Starting bid
    # Provide url for image (optional)
    # Category (optional)
def create_listing(request):
    pass


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
