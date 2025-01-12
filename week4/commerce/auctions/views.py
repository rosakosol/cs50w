from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Listing, Category, Bid, BidForm, Comment, CommentForm, Watchlist, WatchlistForm, CreateForm


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


# Display listing page
def listing_page(request, listing_id):
    # Get the current logged-in user
    user = request.user
    
    # Get listing by unique id
    listing = Listing.objects.get(pk=listing_id)
    category = listing.category
    comments = listing.comments.all().order_by('-created_at')
    
    # Pagination for comments
    paginator = Paginator(comments, 3)  # Show 10 comments per page
    page_number = request.GET.get("page")  # Get the page number from the URL query string
    page_obj = paginator.get_page(page_number)  # Get the page of comments
    
    # If user is logged in:
    if user.is_authenticated:
        if request.method == "POST":
            watchlist_form = WatchlistForm(request.POST)
            if watchlist_form.is_valid():
                action = watchlist_form.cleaned_data["action"]

                if action == "add":
                    # Check if listing is already in user's watchlist
                    if not Watchlist.objects.filter(user=user, listing=listing).exists():
                        Watchlist.objects.create(user=user, listing=listing)
                        messages.success(request, "Item added to watchlist.")
                        
                # Handle removing the listing from the watchlist
                elif action == 'remove':
                    
                    watchlist_item = Watchlist.objects.filter(user=request.user, listing=listing).first()
                    if watchlist_item:
                        watchlist_item.delete()
                        messages.error(request, "Item removed from watchlist.")
                        

                # After the action, render the same listing page with the updated data
                return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))
            
            
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = Comment()
                new_comment.content = comment_form.cleaned_data["content"]
                new_comment.user = user
                new_comment.listing = listing
                new_comment.save()              
                return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))  # Redirect to the same page to show the new comment

            bid_form = BidForm(request.POST)  # Bind form with POST data
            if bid_form.is_valid():
                bid = Bid()
                bid.current = bid_form.cleaned_data["bid_amount"]
                highest_bid = listing.current_highest_bid()
                
                # If bid is valid
                if bid.current > highest_bid.current and bid.current >= listing.starting_bid:
                    bid.user = user
                    bid.listing = listing
                    bid.save()
                    listing.refresh_from_db()
                    bid_message = "Your bid has been placed successfully!"
                    # Refresh the bid form
                    bid_form = BidForm()
                    
                # Else if bid is invalid
                else:
                    bid_message = "Your bid must be higher than the current bid."
                    # Refresh the bid form
                    bid_form = BidForm()
            else:
                # Refresh the bid form
                bid_form = BidForm()
        else:
            bid_form = BidForm()
            comment_form = CommentForm() 
            watchlist_Form = WatchlistForm()
            bid_message = None
            is_watched = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    # If user isn't signed in, they cannot bid or write comments
    else:
        bid_form = None
        comment_form = None
        bid_message = None
        is_watched = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    
    return render(request, 'auctions/listing.html', {
        "user": user,
        "listing": listing,
        "category": category,
        "comments": comments,
        "page_obj": page_obj,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "bid_message": bid_message,
        "is_watched": is_watched
    })

        
# Close auctions if user is the creator of listing
def update_listing_status(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    
    # Close auction by setting listing status to inactive
    listing.is_active = False
    winning_bid = listing.current_highest_bid()
    
    if winning_bid != listing.starting_bid:
        listing.winning_bidder = winning_bid.user
        listing.save()
        messages.warning(request, "The auction has been closed.")
    else:
        # Handle case where there are no bids
        listing.winning_bidder = None
        listing.save()
    
    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))
        
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
    # Get the current logged-in user
    user = request.user
    listings = Listing.objects.all()
    
    if user.is_authenticated:
        # Display watchlist
        watchlist = Watchlist.objects.filter(user=user)
    else:
        watchlist = []
    
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "listings": listings,
        "watchlist": watchlist
    })


# If user is logged in, they can create a new listing
    # Title
    # Description
    # Starting bid
    # Provide url for image (optional)
    # Category (optional)
def create_listing(request):
    user = request.user
    listings = Listing.objects.all()
    
    if user.is_authenticated:
        if request.method == "POST":
            create_form = CreateForm(request.POST)
            if create_form.is_valid():
                new_listing = Listing()
                new_listing.name = create_form.cleaned_data["name"]
                new_listing.description = create_form.cleaned_data["description"]
                new_listing.starting_bid = create_form.cleaned_data["starting_bid"]
                new_listing.image_url = create_form.cleaned_data["image_url"]
                new_listing.creator = user
                new_listing.category = create_form.cleaned_data["category"]
                new_listing.save()              
                return HttpResponseRedirect(reverse("listing_page", args=[new_listing.id]))  # Redirect to the same page to show the new comment
        
        else:
            create_form = CreateForm()
        
    return render(request, "auctions/create_listing.html", {
        "user": user,
        "create_form": create_form,
    })
        


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
