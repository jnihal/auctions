from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    product_name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    category = models.CharField(max_length=64, blank=True)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    current_bid_user = models.CharField(max_length=64)
    image = models.URLField(blank=True)
    date = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.owner.username}: {self.product_name}"


class Bid(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_value = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    date = models.CharField(max_length=64)

    def __str__(self):
        return f"₹{self.bid_value} by {self.person.username} on {self.date}"


class Comment(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1024)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.date} {self.person.username}: {self.comment}"


class Watchlist(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)