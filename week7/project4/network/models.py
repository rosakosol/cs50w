from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone
from django.views.generic import ListView


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, default=None)
    profile_picture = models.ImageField(upload_to="images/User/%d/%m/%y", default="profile-default.webp")
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, default=None, null=True)
    image = models.ImageField(upload_to="images/Post/%d/%m/%y")
    
class PostView(ListView):
    paginate_by = 10
    model = Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']
        widgets = {
            'content': forms.Textarea()
        }
    

class Follow(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"
    
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(blank=True, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

class CommentForm(forms.Form):
    content = forms.CharField(
        label="",
        widget=forms.Textarea()
    )
