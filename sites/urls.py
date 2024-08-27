from django.urls import path

from sites.views import test


urlpatterns = [
    path("", test),
]
