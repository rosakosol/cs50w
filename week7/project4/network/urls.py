
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("access_denied", views.access_denied, name="access_denied")
] 


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
