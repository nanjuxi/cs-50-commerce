from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionList
from .forms import NewAuction


def index(request):
    a = AuctionList.objects.exclude(closed=True)
    # for listing in a:
    #     print(listing.pk)
    return render(request, "auctions/index.html", {
        "activelistings": AuctionList.objects.exclude(closed=True),
        "closedlistings": AuctionList.objects.filter(closed=True)
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

def add(request):
    return render(request, "auctions/add.html", {
        "NewAuction": NewAuction(),
    })

def CreateList(request):
    if request.method == "POST":
        form = NewAuction(request.POST)
        form.save()
        return render(request, "auctions/index.html", {
              "activelistings": AuctionList.objects.exclude(closed=True),
              "closedlistings": AuctionList.objects.filter(closed=True)
        })

def ListPage(request, listing_id):
    if request.user.is_authenticated:
        auction = AuctionList.objects.get(pk=listing_id)
        return render(request, "auctions/ListPage.html", {
            "auction": auction,
        })
    else:
        return render(request, "auctions/index.html")





