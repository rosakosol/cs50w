from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


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
    
    listing = Listing.objects.get(pk=listing_id)
    
    return render(request, "auctions/listing.html", {
        "listing": listing
    })
        

# Watchlist of listings
def watchlist(request):
    pass

# Display all categories of listings
def categories(request):
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
