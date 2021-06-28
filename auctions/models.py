from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField


class User(AbstractUser):
    pass

class listings(models.Model):
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    time = models.CharField(max_length=20)
    details = models.CharField(max_length=128)
    imgUrl = models.CharField(max_length=256, default='default_img.PNG')
    category = models.CharField(max_length=13, default='None')

    def __str__(self):
        return f'{self.item_id}: {self.name}'

class bids(models.Model):
    amount = models.IntegerField()
    time = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.bid_id}: {self.amount} at {self.time}'

class comments(models.Model):
    rank = models.IntegerField()
    content = models.CharField(max_length=64)
    time = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.comment_id}: {self.content} at {self.time}'