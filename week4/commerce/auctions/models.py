from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)





class Listing(models.Model):
    pass


class Bid(models.Model):
    pass

class Comment(models.Model):
    pass


