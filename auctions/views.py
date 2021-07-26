from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.query import EmptyQuerySet, prefetch_related_objects
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Watchlist, Comment, Bid
from datetime import datetime
from django import forms


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

        #empty row code:
        current_user = User.objects.get(username=request.user.username)
        a1 = Watchlist(user=current_user)
        a1.save()

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
        listedBy = request.user.username
        closed = False

        if imgUrl == '':
            imgUrl = '/static/auctions/default_img.png'

        item = Listing.objects.create(name=name, price=price, time=time, details=details, imgUrl=imgUrl, category=category, listedBy=listedBy, closed=closed)
        item.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create.html')


def listing(request, item):
    all_amounts = []
    item_id = Listing.objects.get(name=item).id
    if Bid.objects.filter(listing=item_id).exists():
        #get highest value
        for listing in Bid.objects.filter(listing=item_id):
            all_amounts.append(listing.amount)
            all_amounts.sort(reverse=True)
        highest_bid = all_amounts[0] + 1
    else:
        highest_bid = Listing.objects.get(name=item).price + 1

    class MakeBidForm(forms.Form):
        bid = forms.IntegerField(label='Make Bid', min_value=highest_bid)

    if request.method == 'POST':

        #watchlist
        if request.POST['button'] == 'Watchlist':
            item_id = Listing.objects.get(name=item).id
            query_set = Watchlist.objects.filter(user=request.user.id, listings=item_id)
            if query_set.exists():
                #remove
                watchlist = Watchlist.objects.get(user=request.user.id)
                watchlist.listings.remove(Listing.objects.get(name=item))
            else:
                #add
                watchlist = Watchlist.objects.get(user=request.user.id)
                watchlist.listings.add(Listing.objects.get(name=item))

        #make bid
        '''if request.POST['bid-box'] != 'None':
            bid = int(request.POST['bid-box'])'''
        form = MakeBidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
        
        #close bid
        if request.POST['bid-box'] == 'close':
            pass
    
        #comment
        if request.POST['comment'] != 'None':
            c = Comment(content=request.POST['comment'], time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), by=User.objects.get(id=request.user.id), listing=Listing.objects.get(name=item))
            c.save()

        return HttpResponseRedirect(reverse('listing', args=(item, )))

    else:
        item_id = Listing.objects.get(name=item).id
        query_set = Watchlist.objects.filter(user=request.user.id, listings=item_id)
        if query_set.exists():
            button = 'Remove from Watchlist'
        else:
            button = 'Add to Watchlist'
        
        try:
            if Bid.objects.get(amount=highest_bid-1).by == request.user.id:
                isHighestBid = True
            else:
                isHighestBid = False
        except:
            isHighestBid = False

        numOfBids = len(all_amounts)

        return render(request, 'auctions/listing.html', {
                'item': Listing.objects.get(name=item),
                'button': button,
                'comments': Comment.objects.filter(listing=item_id),
                'bidform': MakeBidForm(),
                'isHighestBid': isHighestBid,
                'numOfBids': numOfBids,
                'highest_bid': highest_bid
        })


def watchlist(request):
    
    if Watchlist.objects.all().filter(user=request.user.id)[0].listings.all().exists():
        items = Watchlist.objects.all().filter(user=request.user.id)[0].listings.all()
    else:
        items = ''

    return render(request, 'auctions/watchlist.html', {
        'items': items
    })


def categories_all(request):
    return render(request, 'auctions/categories.html')


def category(request, category):
    return render(request, 'auctions/category.html', {
        'items': Listing.objects.filter(category=category),
        'category': category 
    })