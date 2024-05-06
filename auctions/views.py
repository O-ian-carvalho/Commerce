from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Categories
from datetime import datetime

from .models import User, Auctions, Comments, Bids, Watchlist, Categories

def index(request):
    listing = Auctions.objects.all()
    categories = Categories.objects.all()
    cate = 'blank'
    if request.method == "POST" and request.POST["categories"]:
        listing = Auctions.objects.filter(categorie=Categories.objects.get(pk=request.POST['categories'])) 
        cate = Categories.objects.get(pk=request.POST['categories'])
    return render(request, "auctions/index.html",{
        "listings": listing,
        "categories": categories,
        "selectedcategorie": cate
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


def create(request):
    if request.method == "POST":
        auction = Auctions(title=request.POST['title'], price=request.POST['price'], active=True,image=request.POST["image"], categorie=Categories.objects.get(pk=request.POST["categorie"]), user= User.objects.get(pk=request.user.id), description=request.POST["description"])
        auction.save()
    categories = Categories.objects.all()
    return render(request, "auctions/create.html",{
        "categories": categories
    })

def showauction(request, auction):
    auction = Auctions.objects.get(pk=auction)
    biggestbid = Bids.objects.filter(auction=auction).order_by('-bid').first()
    if biggestbid is None:
        class MeuObjeto:
            def __init__(self, auction):
                self.bid = auction
            def bid(self):
                return self.bid
        biggestbid = MeuObjeto(auction.price)
    getcoments = Comments.objects.filter(auction=auction)
    inwatchlist = False
    if request.user.is_authenticated:
        if Watchlist.objects.filter(user=User.objects.get(pk=request.user.id), auction=auction):
            inwatchlist = True


    message = '';
    if request.method == "POST":
        if request.POST['todo'] == 'watchlist':
            if inwatchlist:
                Watchlist.objects.get(user=User.objects.get(pk=request.user.id), auction=auction).delete()
                inwatchlist = False
            else:
                Watchlist(user=User.objects.get(pk=request.user.id), auction=auction).save()
                inwatchlist = True


        if request.POST['todo'] == "comment":
            date= datetime.now()
            comment = Comments(text=request.POST["textarea"], user=User.objects.get(pk=request.user.id), auction=auction, day=date.day, month=date.month, year=date.year)
            comment.save()
        if request.POST['todo'] == 'close':
            Auctions.objects.filter(pk=auction.pk).update(active=False)
            return HttpResponseRedirect(reverse('index'))
        if request.POST['todo'] == "mekebid":
            if int(request.POST['bid']) <= biggestbid.bid:
                message = f"Type a value grather than {biggestbid.bid}"
            else:
                bid = Bids(user=User.objects.get(pk=request.user.id), auction=auction, bid=int(request.POST['bid']))
                bid.save()
                Auctions.objects.filter(pk=auction.pk).update(biggest_bid=int(request.POST['bid']))
                if not inwatchlist:
                    Watchlist(user=User.objects.get(pk=request.user.id), auction=auction).save()
                    inwatchlist = True
    biggestbid = Bids.objects.filter(auction=auction).order_by('-bid').first()
    return render(request, "auctions/item.html",{
        'auction': auction,
        'comments': getcoments,
        'biggestbid': biggestbid,
        'message': message,
        'inwatchlist':inwatchlist
    })



def watchlist(request):
    listings = Watchlist.objects.filter(user=User.objects.get(pk=request.user.id))
    return render(request, 'auctions/watchlist.html',{
    'listings': listings
    }
    )

def categories(request):
    categories = Categories.objects.all()
    return render(request, 'auctions/categories.html',{
        'categories': categories
    })

def categorie(request, categorie):
    return HttpResponse("haha")