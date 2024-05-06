from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

class Auctions(models.Model):
    title = models.CharField(max_length=40, unique=True)
    price = models.IntegerField()
    active = models.BooleanField()
    image = models.CharField(max_length=20000)
    description = models.CharField(max_length=120)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="auctions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    biggest_bid = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="buyers")
    bid = models.IntegerField()
    def __str__(self):
        return f"{self.bid}"

class Comments(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="comments")
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()


    def __str__(self):
        return f"{self.text}"


class Watchlist(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="wathlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wathlist")

