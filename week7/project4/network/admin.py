from django.contrib import admin
from django.utils import timezone
from .models import User, Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    ordering = ("-created_at",) 
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "content", "created_at")
    list_filter = ("post", "user")
    search_fields = ["content","user"]
    ordering = ("-created_at",)

    
admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)