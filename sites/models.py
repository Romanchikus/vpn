from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse

from user.models import User


alphanumeric = RegexValidator(
    r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
)


class Site(models.Model):
    url = models.URLField(max_length=256, unique=True)
    name = models.CharField(max_length=64, unique=True, validators=[alphanumeric])
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_app_link_to_site(self, absolute_uri):
        return f"{absolute_uri}{self.name}/"

    def get_absolute_url(self):
        return reverse("base_site_url", kwargs={"name": self.name})


class Activity(models.Model):

    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    content_size = models.FloatField()
    route = models.CharField(max_length=128)
