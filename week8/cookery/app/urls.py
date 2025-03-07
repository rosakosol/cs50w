from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_recipe/", views.add_recipe_view, name="add_recipe"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("recipe/<str:recipe_name>", views.recipe, name="recipe"),
    path("edit_recipe/<int:recipe_id>/", views.edit_recipe, name="edit_recipe"),
    path("delete_recipe/<int:recipe_id>/", views.delete_recipe, name="delete_recipe"),
    path("favourites/", views.favourites_view, name="favourites"),
    path("search/", views.search, name="search"),
    path("sort/", views.sort, name="sort"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)