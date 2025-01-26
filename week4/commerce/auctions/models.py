from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    winning_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winning_bidder_listings", null=True)
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_listings', default=1)
    
    def __str__(self):
        return self.name
    
    def current_highest_bid(self):
        # self.bids is a reverse relationship to Bid model -> gets all bids linked to listing
        highest_bid = self.bids.all().order_by('-current').first()
        if highest_bid:
            return highest_bid
        else:
            # If there are no other bids other than the starting bid, return False
            return False


# Custom Validator for starting bids using Create New Listing Form
def validate_bid(value):
    if value >= 0.01:
        return value
    else:
        raise ValidationError("Bid must be at least $0.01.")

class CreateForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(
        label='Content',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 80
        }))
    starting_bid = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[validate_bid]
    )
    image_url = forms.URLField(max_length=200, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched_by")
    added_at = models.DateTimeField(auto_now_add=True) 
    
class WatchlistForm(forms.Form):
    listing_id = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=[('add', 'Add'), ('remove', 'Remove')], widget=forms.HiddenInput())

    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', default=1)
    current = models.DecimalField(default=0.01, max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.current} by {self.user}"
    
    
class BidForm(forms.Form):
    bid_amount = forms.DecimalField(
        label='Bid Amount',
        max_digits=10,  # Adjust the total digits allowed (including the decimal part)
        decimal_places=2,  # Ensure only 2 decimal places
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter bid amount',
            'min': '0.01',
            'step': '0.01'
        })
    )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default=1)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"

class CommentForm(forms.Form):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 80
        })
    )

