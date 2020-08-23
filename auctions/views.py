from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "objectForLoop": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            #get all details including current user
            listingName = request.POST["listingName"]
            currentBid = request.POST["currentBid"]
            listingDescription = request.POST["listingDescription"]
            listingCategories = request.POST.getlist("category")
            imgURL = request.POST["imgURL"]
            currentUser = User.objects.get(pk=request.user.id)

            #create new listing
            newListing = Listing.objects.create(owner=currentUser, listingItemName=listingName, currentBid=currentBid, 
                            listingDescription=listingDescription, imgURL=imgURL)

            #filter list for categories
            for cat in listingCategories:
                newListing.categories.add(Category.objects.get(categoryName=cat))

            newListing.save()

            #change to lead to "my listing page" instead
            return HttpResponseRedirect(reverse("index")) 
        else:
            return render(request, "auctions/createListing.html", {
                "categories": Category.objects.all()
            })
    else:
        return HttpResponseRedirect(reverse("index"))


def watchlistAdd(request, watchlistItemID):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        currentUser = User.objects.get(pk=request.user.id)     
        currentUser.watchlist.add(Listing.objects.get(pk=watchlistItemID))

        return HttpResponseRedirect(reverse("watchlist"))
    else:
        return HttpResponseRedirect(reverse("index"))

def watchlistRemove(request, watchlistItemID):
    if request.method == "POST":
        currentUser = User.objects.get(pk=request.user.id)
        currentUser.watchlist.remove(Listing.objects.get(pk=watchlistItemID))
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        return HttpResponseRedirect(reverse("index"))

def watchlist(request):
    #for showing watchlist
    return render(request, "auctions/watchlist.html",
    {
        "objectForLoop": request.user.watchlist.all()
    })

def categories(request):
    return render(request, "auctions/categories.html",
    {
        "categories": Category.objects.all()
    })

def categoryItems(request, categoryName):
    selectedCategory = Category.objects.get(categoryName=categoryName)
    itemsInCategory = selectedCategory.itemsInCategory.all()
    return render(request, "auctions/categoryItem.html",
    {
        "objectForLoop": itemsInCategory,
        "categoryName": categoryName
    })

def viewlistinginfo(request, listingID):
    return render(request, "auctions/listingInfo.html", {
        "listing": Listing.objects.get(pk=listingID)
    })

def updateCurrentBid(request):
    pass