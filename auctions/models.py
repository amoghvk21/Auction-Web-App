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
    listedBy = models.CharField(max_length=256, blank=False)
    closed = models.BooleanField(default=False)
    winner = models.CharField(default='None', max_length=256)

    def __str__(self):
        return self.name

class Bid(models.Model):
    amount = models.IntegerField()
    time = models.CharField(max_length=20)
    listing = models.ForeignKey(Listing, blank=False, on_delete=models.DO_NOTHING)
    by = models.ForeignKey(User, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.amount} at {self.time} for {self.listing} by {self.by}'

class Comment(models.Model):
    content = models.CharField(max_length=64)
    time = models.CharField(max_length=20)
    by = models.ForeignKey(User, blank=False, null=False, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(Listing, blank=False, null=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'"{self.content}" at {self.time} by {self.by}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='watchlist')
    listings = models.ManyToManyField(Listing, blank=True, null=True, related_name='watchlist')

    def __str__(self):
        return f'{self.user}''s watchlist' 