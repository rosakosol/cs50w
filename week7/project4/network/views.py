from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import random

from .models import User, Post, PostForm, Follow, Like


def index(request):
    user = request.user
    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # If user is logged in, show new post form
    if user.is_authenticated:
            if request.method == "POST":
                post_form = PostForm(request.POST, request.FILES)
                if post_form.is_valid():
                    new_post = Post()
                    new_post.user = user
                    new_post.content = post_form.cleaned_data["content"]
                    new_post.image = post_form.cleaned_data["image"]
                    new_post.save()
                    
                    return HttpResponseRedirect(reverse("index"))
                
            else:
                post_form = PostForm()
    else:
        post_form = None
        
    return render(request, "network/index.html", {
        "user": user,
        "post_form": post_form,
        "posts": posts,
        "page_obj": page_obj
    })

def like_post(request, post_id):
    user = request.user
    post = None
    
    # Exception handling if post does not exist
    try:
        post = Post.objects.get(pk=post_id)
    except:
        print("Post does not exist.")
        return False
    
    # Check if user has already liked post
    like_exists = Like.objects.filter(post=post, user=user).first()
    
    # If post already liked, delete the like
    if like_exists:
        like_exists.delete()
        liked = False
        
    # Else create a new Like object
    else:
        Like.objects.create(post=post, user=user)
        liked = True
    
    # Count number of likes on post
    like_count = post.likes.count()
    
    return JsonResponse({
        "like_count": like_count, 
        "liked": liked
    })

def profile_view(request, username):    
    # Get User instance from profile username
    profile_user = User.objects.get(username=username)
    
    # Get profile posts
    posts = Post.objects.filter(user=profile_user).order_by("-created_at")
    print(posts.query)
    
    # Check if user is following profile user
    is_following = Follow.objects.filter(users=profile_user, follower=request.user).exists()

    return render(request, "network/profile.html", {
        "posts": posts,
        "profile_user": profile_user,
        "is_following": is_following,
    })

def follow_user(request, username):
    user = request.user
    profile_user = None
    
    # Exception handling if profile user does not exist
    try:
        profile_user = User.objects.get(username=username)
        following_user = Follow.objects.filter(users=profile_user, follower=user)
    except:
        print("Profile does not exist.")
        return False
    
    
    # If user already following, then delete follow from list
    if following_user.exists():
        following_user.delete()
        followed = False
        
    # Else create a new Follow object
    else:
        Follow.objects.create(users=profile_user, follower=user)
        followed = True

    # Get the follower count for the profile user
    follow_count = profile_user.followers.count()
    
    return JsonResponse({
        "follow_count": follow_count, 
        "followed": followed
    })
    
def following_view(request):
    user = request.user
    
    if user.is_authenticated:
        followed_users = Follow.objects.filter(follower=user).select_related("users")
        followed_user_ids = followed_users.values_list("users", flat=True)
        
        # If user is following others
        if followed_users:
            posts = Post.objects.filter(user__id__in=followed_user_ids)
            
            random_posts = random.sample(list(posts), min(5, len(posts)))
        else:
            random_posts = None
        
    return render(request, "network/following.html", {
        "user": user,
        "followed_users": followed_users,
        "random_posts": random_posts
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
