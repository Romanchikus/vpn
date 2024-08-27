from django.urls import path

from sites.views import test, get_site_url


urlpatterns = [
    path("", test),
    path("<str:name>/", get_site_url, name="base_site_url"),
]
