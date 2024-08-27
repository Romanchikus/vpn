from django.db import models
from user.models import User


class Site(models.Model):
    url = models.URLField(max_length=256, unique=True)
    name = models.CharField(max_length=64, unique=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):

    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    content_size = models.FloatField()
    route = models.CharField(max_length=128)
