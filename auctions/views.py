from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from datetime import date, datetime

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    active_listings = Listing.objects.filter(active=True)
    closed_listings = Listing.objects.filter(active=False)
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "closed_listings": closed_listings
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def new(request):
    if request.method == "POST":
        user = request.user
        product_name = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        image = request.POST["image_url"]
        today = date.today()
        day = today.strftime("%B %d, %Y")

        new_listing = Listing(
            owner=user, product_name=product_name, description=description, starting_bid=starting_bid,
            current_bid=starting_bid, category=category, image=image, date=day, current_bid_user=user.username
        )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/newListing.html")


@login_required(login_url="login")
def listing(request, id):
    product = Listing.objects.get(id=id)
    total_bids = len(product.bids.all())
    username = request.user.username
    is_active = product.active
    comments = reversed(Comment.objects.filter(listing=product))

    if request.method == "GET" and 'watchlist' in request.GET:
        add_watchlist = Watchlist(person=request.user, listing=product)
        add_watchlist.save()
    elif request.method == "GET" and 'rem_watchlist' in request.GET:
        Watchlist.objects.filter(person=request.user, listing=product).delete()
    
    if request.method == "GET" and 'close' in request.GET:
        product.active = False
        product.save()
        Watchlist.objects.filter(listing=product).delete()
        return HttpResponseRedirect(reverse("listing", args=[id]))

    try:
        watchlist = Watchlist.objects.get(person=request.user, listing=product)
        watchlist = True
    except Watchlist.DoesNotExist:
        watchlist = False

    if total_bids == 0:
        bid_info = "0 bid(s) so far."
    elif username == product.current_bid_user:
        bid_info = f"{total_bids} bid(s) so far. Your bid is the highest."
    else:
        bid_info = f"{total_bids} bid(s) so far. {product.current_bid_user}'s bid is the highest."

    if username == product.owner.username:

        return render(request, "auctions/listing.html", {
            "product": product,
            "active": is_active,
            "owner": True,
            "watchlist": watchlist,
            "bid_info": bid_info,
            "bid_details": reversed(product.bids.all()),
            "comments": comments
        })

    else:
        if request.method == "POST":
            bid = request.POST["bid"]
            user = request.user
            day = date.today().strftime("%B %d, %Y")

            if int(bid) <= product.current_bid:
                return render(request, "auctions/listing.html", {
                    "active": is_active,
                    "product": product,
                    "message": "Bid should be greater than the current bid.",
                    "watchlist": watchlist,
                    "bid_info": bid_info,
                    "bid_details": reversed(product.bids.all()),
                    "comments": comments
                })
            
            else:
                new_bid = Bid(
                    person=user, bid_value=bid, listing=product, date=day
                )
                new_bid.save()
                product.current_bid = int(bid)
                product.current_bid_user = username
                product.save()
                bid_info = f"{len(product.bids.all())} bid(s) so far. Your bid is the highest."

        return render(request, "auctions/listing.html", {
            "active": is_active,
            "product": product,
            "bid_info": bid_info,
            "watchlist": watchlist,
            "bid_details": reversed(product.bids.all()),
            "comments": comments
        })

@login_required(login_url="login")
def watchlist(request):
    watchlists = Watchlist.objects.filter(person=request.user)
    listings = [watchlist.listing for watchlist in watchlists]
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url="login")
def comment(request, id):
    if request.method == "POST":
        comment = request.POST["comment"]
        new_comment = Comment(
            person=request.user,
            comment=comment,
            listing=Listing.objects.get(id=id),
            date=date.today().strftime("%B %d, %Y")
        )
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[id]))

    return render(request, "auctions/comment.html", {
        "id": id
    })


def category(request, name):
    active_listings = Listing.objects.filter(active=True, category=name)
    closed_listings = Listing.objects.filter(active=False)
    return render(request, "auctions/category.html", {
        "category": name,
        "listings": active_listings,
        "closed_listings": closed_listings
    })
    