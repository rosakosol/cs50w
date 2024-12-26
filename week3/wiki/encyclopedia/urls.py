from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/new", views.new, name="new"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry")

]