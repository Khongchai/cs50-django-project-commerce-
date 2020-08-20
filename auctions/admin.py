from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listingItemName", "listingPrice", "listingDate", "imgURL")
    filter_horizontal = ("categories",)
# Register your models here.

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)