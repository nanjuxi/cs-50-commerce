from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Max


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

@login_required
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
        currentuser = UserList.objects.filter(auctionlist_id = auction, user_id = request.user)
        check = WatchList.objects.filter(auctionlist_id=auction, user_id=request.user)
        winner = False
        if request.user == auction.winner:
            winner = True
        return render(request, "auctions/ListPage.html", {
            "auction": auction,
            "currentbid": Bid.objects.filter(auctionlist_id = auction).aggregate(Max('bid')),
            "check": check,
            "form": BidForm(),
            "close": currentuser,
            "winner": winner,
            "commentform": CommentForm(),
            "comments": Comments.objects.filter(auctionslist_id=auction)
        })
    else:
        auction = AuctionList.objects.get(pk = listing_id)
        currentbid = Bid.objects.filter(auctionlist_id = auction)
        if currentbid:
            bid = currentbid.aggregate(Max('bid'))
            return render(request, "auctions/ListPage.html", {
                "listing": AuctionList.objects.get(pk=listing_id),
                "currentbid": bid,
                "commentform": CommentForm(),
                "comments": Comments.objects.filter(auctionslist_id=auction),
            })
        else:
            return render(request, "auctions/ListPage.html", {
                "listing": AuctionList.objects.get(pk=listing_id),
                "currentbid": None,
                "commentform": CommentForm(),
                "comments": Comments.objects.filter(auctionslist_id=auction)
            })


def addwatchlist(request, listing_id):
    print("1")
    if request.method == "POST":
        watch = WatchList(user_id=1, auctionlist_id=listing_id)
        watch.save()
        print("2")
        return(render, "auctions/ListPage.html", {
        })
    print("3")




