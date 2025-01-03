from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.

# Admin able to view listing creation date, end date, duration, price, location
class ListingAdmin(admin.ModelAdmin):
    pass
    
# Admin able to view history of all bids on a listing from date
class BidAdmin(admin.ModelAdmin):
    pass
    
# Admin able to delete and edit comments
class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
