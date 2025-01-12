from django.contrib import admin
from django.utils import timezone

from .models import User, Listing, Bid, Comment, Category

# Register your models here.

# Admin able to view and edit categories
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',) 

# Admin able to view and edit listing creation date, end date, duration, price, location
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'starting_bid', 'winning_bidder', 'winning_bid', 'created_at', 'is_active', 'image_url')
    readonly_fields = ["creator", "winning_bidder"]
    search_fields = ('name', 'category_name')
    ordering = ('created_at',) 
    
    def winning_bidder(self, obj):
        highest_bid = obj.current_highest_bid()
        
        if highest_bid != obj.starting_bid:
            return highest_bid.user
        else:
            return "N/A"
    winning_bidder.short_description = 'Winning Bidder'

    def winning_bid(self, obj):
        highest_bid = obj.current_highest_bid()
        
        if highest_bid != obj.starting_bid:
            return highest_bid.current
        else:
            return "N/A"
    winning_bid.short_description = 'Winning Bid'
    

    
# Admin able to view history of all bids on a listing from date
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'user', 'current', 'created_at')
    search_fields = ('listing__name', 'user__username')
    list_filter = ('listing', 'user')
    ordering = ('-created_at',)
    
# Admin able to delete and edit comments
class CommentAdmin(admin.ModelAdmin):
        # Override the list_display to display times in local time zone instead of default UTC
        def created_at_local(self, obj):
            return timezone.localtime(obj.created_at).strftime('%d-%m-%Y %H:%M:%S')

        created_at_local.admin_order_field = 'created_at'
        created_at_local.short_description = 'Created at (Local Time)'
        
        list_display = ('id', 'user', 'listing', 'content', 'created_at_local')
        search_fields = ('user__username', 'listing__name', 'content')
        list_filter = ('listing', 'user')
        ordering = ('-created_at',)
    


admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
