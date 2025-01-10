from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone

class User(AbstractUser):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    
        
class Category(models.Model):
    name = models.CharField(max_length=64, null=True)
    
    def __str__(self):
        return self.name

class Listing(models.Model):
    name = models.CharField(max_length=64, default="Listing")
    description = models.TextField(null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def current_highest_bid(self):
        # self.bids is a reverse relationship to Bid model -> gets all bids linked to listing
        highest_bid = self.bids.order_by('-current').first()
        return highest_bid.current if highest_bid else self.starting_bid

    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', default=1)
    current = models.DecimalField(default=0.01, max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.current} by {self.user} on {self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default=1)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"


