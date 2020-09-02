from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:categoryName>", views.categoryItems, name="categoryItems"),
    path("viewlistinginfo/<int:listingID>", views.viewlistingAndUpdateInfo, name="viewlistingAndUpdateInfo"),
    path("closebid/<int:listingID>", views.closeBid, name="closeBid"),
    path("watchlistAddRemove", views.watchlistAddRemove, name="watchlistAddRemove")

]
