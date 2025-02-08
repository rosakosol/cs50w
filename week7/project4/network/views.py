from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, PostForm, Follow, Like


def index(request):
    user = request.user
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if user.is_authenticated:
            if request.method == "POST":
                post_form = PostForm(request.POST, request.FILES)
                if post_form.is_valid():
                    new_post = Post()
                    new_post.author = user
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
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        print("Post does not exist.")
        return False
    
    # Check if user has already liked post
    like_exists = Like.objects.filter(post=post, user=user).first()
    
    if like_exists:
        like_exists.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=user)
        liked = True
    
    like_count = post.likes.count()
    return JsonResponse({"like_count": like_count, "liked": liked})

def profile_view(request, username):
    user = request.user
    followers = user.followers.count()
    following = user.following.count()
    
    # If not user profile, display follow/unfollow button
    
    
    
    
    return render(request, "network/profile.html", {
        "user": user,
        "followers": followers,
        "following": following
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
