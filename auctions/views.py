from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
from .models import *


def index(request):
    #begin with only five posts
    start = 0
    end = 5
    listings = (Listing.objects.all())[start:end]
    return render(request, "auctions/index.html", {
        "objectForLoop": listings
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

            #the owner is the immediate highest bidder
            newListing = Listing.objects.create(owner=currentUser, listingItemName=listingName, currentBid=currentBid, 
                            listingDescription=listingDescription, imgURL=imgURL, currentHighestBidOwner=currentUser)

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


@login_required
@csrf_exempt
def watchlistAddRemove(request):
    if request.method != "PUT":
        return JsonResponse({
            "error": "PUT method required."
        }, status=400)
    data = json.loads(request.body)    
    operation = data.get("operation")
    watchlistItemID = data.get("listingID")
    requestedObject = Listing.objects.get(pk=watchlistItemID)
    currentUser = User.objects.get(pk=request.user.id) 

    #change text from server is actually good, cus it ensures that
    #button text is changed as a respond to the success of data manipulation
    if requestedObject not in currentUser.watchlist.all():
        currentUser.watchlist.add(Listing.objects.get(pk=watchlistItemID))
        currentUser.save()
        return JsonResponse({
            "newButtonText": "Remove from Watchlist"
        }, status=201)
    else:
        currentUser.watchlist.remove(Listing.objects.get(pk=watchlistItemID))
        currentUser.save()
        return JsonResponse({
            "newButtonText": "Add to Watchlist"
        }, status=201)

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

def viewlistingAndUpdateInfo(request, listingID):

    listing = Listing.objects.get(pk=listingID)
    print(listing)
    if request.method == "POST":
        newBid = request.POST["newBid"]
        newBidder = User.objects.get(pk=request.user.id)
        if listing.currentBid < int(newBid):
            listing.currentBid = newBid
            listing.currentHighestBidOwner = newBidder
            listing.save()
        else:
            #TODO pass error message that new bid should be higher than current
            return render(request, "auctions/listingInfo.html", {
            "listing": listing,
            "errorMessage": "New bid should be higher than the current bid"
        })
        
    return render(request, "auctions/listingInfo.html", {
        "listing": listing
    })

def closeBid(request, listingID):
    listing = Listing.objects.get(pk=listingID)
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html")

    closingPrice = int(request.POST["closingPrice"])
    if listing.currentBid < closingPrice:
        return render(request, "auctions/listingInfo.html", {
        "listing": listing,
        "errorMessage": "New bid should be higher than the current bid"
    })
    else:
        listing.currentBid = closingPrice
        listing.active = False
        listing.save()
        #after having checked that last bid is valid, begin the process of closing off this bid
        return render(request, "auctions/listingInfo.html", {
        "listing": listing
    })

def loadListings(request):
    start = int(request.GET.get("start"))
    end = int(request.GET.get("end"))
    listings = list((Listing.objects.values())[start:end])
    #serialize object then return as json
    print(listings)
    return JsonResponse({
        "listings": listings
    })
        
    