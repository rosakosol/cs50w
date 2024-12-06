from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry")
]

print("encyclopedia URL patterns:", urlpatterns)