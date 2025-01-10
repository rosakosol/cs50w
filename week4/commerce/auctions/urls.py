from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<str:listing_name>", views.listing_page, name="listing"),
    path("login", views.login_view, name="login"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
