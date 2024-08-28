from django.urls import path, re_path

from sites.views import test, get_site_url, get_site_route_url


urlpatterns = [
    path("", test),
    re_path(r"^(?P<name>[\w-]+)/.+$", get_site_route_url, name="site_route_url"),
    path("<str:name>/", get_site_url, name="base_site_url"),
]
