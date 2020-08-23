from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("watchlistadd/<int:watchlistItemID>", views.watchlistAdd, name="watchlistAdd"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlistRemove/<int:watchlistItemID>", views.watchlistRemove, name="watchlistRemove"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:categoryName>", views.categoryItems, name="categoryItems"),
    path("viewlistinginfo/<int:listingID>", views.viewlistinginfo, name="viewlistinginfo"),
    path("updateCurrentBid", views.updateCurrentBid, name="updateCurrentBid")
]
