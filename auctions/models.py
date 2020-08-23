from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="usersWatchlist")
    bio = models.TextField(max_length=500, blank=True)

class Category(models.Model):
    categoryName = models.TextField(default="Enter Name")

    def __str__(self):
        return f"{self.categoryName}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listedProducts")
    currentHighestBidOwner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="highestBidderOn", null=True)
    listingItemName = models.CharField(max_length=64)
    currentBid = models.IntegerField(default=1, null=False, blank=False)
    listingDate = models.DateTimeField(auto_now_add=True, blank=True)
    listingDescription = models.TextField(default="Enter description")
    #null = value is null in the database
    #blank = whether user is required to fill this field the form or not
    imgURL = models.URLField(max_length=200, null=True, blank=False)
    categories = models.ManyToManyField(Category, blank=True, related_name="itemsInCategory")

    def __str__(self):
        return f"ID: {self.id}\n Product: {self.listingItemName}\n Posted by: {self.owner} \n Price: {self.currentBid} \n Listing date: {self.listingDate} \n imgURL: {self.imgURL}\n Categories: {self.categories}"

class Comment(models.Model):
    content = models.TextField(default="Enter comment")
    commentedOn = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    #do not delete comments when users are deleted.
    commentor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="commentor", null=True, blank=True)
    commentedDate = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"comment: {self.content}\nComment on: {self.commentedOn}\nCommentor: {self.commentor}\ncommentedDate: {self.commentedDate}"



