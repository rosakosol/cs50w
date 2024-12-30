from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)

class Listing(models.Model):
    name = models.CharField(max_length=64, default="Listing")
    description = models.TextField(null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def current_highest_bid(self):
        # Returns the highest bid for the listing (if any)
        highest_bid = self.bids.order_by('-current').first()
        return highest_bid.current if highest_bid else self.starting_bid
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', default=1)  # Who placed the bid
    current = models.DecimalField(default=0.01, max_digits=10, decimal_places=2)  # The bid amount
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=1)  # The listing the bid is for
    created_at = models.DateTimeField(default=timezone.now)  # When the bid was placed

    def __str__(self):
        return f"Bid of {self.current} by {self.user} on {self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # User who made the comment
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default=1)  # The listing the comment is for
    content = models.TextField(null=True)  # The content of the comment
    created_at = models.DateTimeField(default=timezone.now)  # When the comment was made

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"


