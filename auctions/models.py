from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.query_utils import select_related_descend

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    time = models.CharField(max_length=20)
    details = models.CharField(max_length=128)
    imgUrl = models.CharField(max_length=256)
    category = models.CharField(max_length=13, default='None')
    #peopleWatching = models.ExpressionList()

    def __str__(self):
        return self.name

class Bid(models.Model):
    amount = models.IntegerField()
    time = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.amount} at {self.time}'

class Comment(models.Model):
    rank = models.IntegerField()
    content = models.CharField(max_length=64)
    time = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.content} at {self.time}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    listings = models.ManyToManyField(Listing, blank=True, related_name='watchlist')

    def __str__(self):
        return f'{self.user}: {self.listings}'