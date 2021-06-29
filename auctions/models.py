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
    imgUrl = models.CharField(max_length=256)
    category = models.CharField(max_length=13, default='None')

    def __str__(self):
        return {
            'name': self.name,
            'price':self.price,
            'time': self.time,
            'details': self.details,
            'imgUrl': self.imgUrl,
            'category': self.category
        }

class bids(models.Model):
    amount = models.IntegerField()
    time = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.amount} at {self.time}'

class comments(models.Model):
    rank = models.IntegerField()
    content = models.CharField(max_length=64)
    time = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.content} at {self.time}'