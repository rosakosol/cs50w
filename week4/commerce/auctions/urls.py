from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<str:listing_name>", views.listing_page, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
