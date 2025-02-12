from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
import random
import json

from .models import User, Post, PostForm, Follow, Like


def index(request):
    # Get logged in user
    user = request.user
    
    # Get all posts sorted newest to oldest
    posts = Post.objects.all().order_by("-created_at")
    
    # Pagination to show 10 posts per page
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
        
        # Else show empty form
        else:
            post_form = PostForm()
                
        # For each post, check if user has liked it to alter button display
        for post in page_obj.object_list:
            post.is_liked = post.likes.filter(user=user).exists()
        
    else:
        post_form = None
    

    return render(request, "network/index.html", {
        "user": user,
        "post_form": post_form,
        "posts": page_obj.object_list,
        "page_obj": page_obj,
    })
    
@login_required
def edit_post(request, post_id):
    # Get logged in user
    user = request.user
    
    # Get post to be edited if it exists
    post = get_object_or_404(Post, pk=post_id)
    
    # If user is not the author, deny access
    if post.user != user:
        return HttpResponseRedirect(reverse("access_denied"))
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_content = data.get('content',)
            post.content = new_content 
            post.save()
            return JsonResponse({
                "success": True,
                "updated_content": post.content
            })
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON data"
            }, status=400)
    return JsonResponse({
        "error": "Invalid request."
    }, status=400)
    
    
def access_denied(request):
    return render(request, "network/access_denied.html",)



def like_post(request, post_id):
    # Get logged in user
    user = request.user
    
    # Get post to be liked if it exists
    post = get_object_or_404(Post, pk=post_id)
    
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
    profile_user = get_object_or_404(User, username=username)
    
    # Get profile posts
    posts = Post.objects.filter(user=profile_user).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Check if user is following profile user
    is_following = Follow.objects.filter(users=profile_user, follower=request.user).exists()

    return render(request, "network/profile.html", {
        "posts": page_obj.object_list,
        "profile_user": profile_user,
        "is_following": is_following,
        "page_obj": page_obj
    })


def follow_user(request, username):
    # Get logged in user
    user = request.user
    
    # Get User instance from profile username
    profile_user = get_object_or_404(User, username=username)
    following_user = Follow.objects.filter(users=profile_user, follower=user)

    
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
    # Get logged in user
    user = request.user

    # If user is logged in
    if user.is_authenticated:
        followed_users = Follow.objects.filter(follower=user).select_related("users")
        followed_user_ids = followed_users.values_list("users", flat=True)
        
        # If user is following others, get a random sample of their posts
        if followed_users:
            posts = Post.objects.filter(user__id__in=followed_user_ids)
            random_posts = random.sample(list(posts), min(5, len(posts)))
        
        else:
            random_posts = None
        
        # Pagination
        paginator = Paginator(random_posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
    return render(request, "network/following.html", {
        "user": user,
        "followed_users": followed_users,
        "random_posts": page_obj.object_list,
        "page_obj": page_obj
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
