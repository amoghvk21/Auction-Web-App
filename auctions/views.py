from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Watchlist
from datetime import datetime


def index(request):
    return render(request, "auctions/index.html", {
        'items': Listing.objects.all()
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
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        details = request.POST['details']
        imgUrl = request.POST['imgUrl']
        category = request.POST['category']

        if imgUrl == '':
            imgUrl = '/static/auctions/default_img.png'

        item = Listing.objects.create(name=name, price=price, time=time, details=details, imgUrl=imgUrl, category=category)
        item.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create.html')


def listing(request, item):
    if request.method == 'POST':
        if request.POST['button'] == 'Watchlist':
            watchlist = Watchlist.objects.get(user=request.user.id)
            watchlist.listings.add(Listing.objects.get(name=item))
        elif request.POST['bid-box'] != 'None':
            pass
        return HttpResponseRedirect(reverse('listing', args=(item, )))
    else:
        try:
            temp = Watchlist.objects.filter(user=User.get_username, listings=item)
            button = 'Remove From Watchlist'
        except:
            button = 'Watchlist'

        return render(request, 'auctions/listing.html', {
                'item': Listing.objects.get(name=item),
                'button': button,
        })