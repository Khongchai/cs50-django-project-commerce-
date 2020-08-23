from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listingItemName", "currentBid", "listingDate", "imgURL")
    filter_horizontal = ("categories",)
# Register your models here.

class UserAdminNew(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

admin.site.register(User, UserAdminNew)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Comment)