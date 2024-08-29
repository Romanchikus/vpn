from typing import Union

from django.http import Http404, HttpResponse
from django.shortcuts import render

from sites.loader import Loader
from sites.models import Site, Activity
from logger import logger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView


class SiteList(LoginRequiredMixin, ListView):
    template_name = "sites.html"
    model = Site
    context_object_name = "sites"

    def get_queryset(self):
        return Site.objects.filter(creator=self.request.user)


@login_required
def add_site(request):
    name = request.POST.get("sitename")
    url = request.POST.get("url")
    name = request.POST.get("sitename")

    # add the site to the user's list
    if not Site.objects.filter(url=url, name=name, creator=request.user).exists():
        Site.objects.get_or_create(
            url=url, name="zaxid", defaults={"creator": request.user}
        )

    # return template fragment with all the user's sites
    sites = Site.objects.filter(creator=request.user)
    return render(request, "partials/site-list.html", {"sites": sites})


@login_required
def get_site_route(site_name: str, path: str) -> str:
    splitted: list[str] = path.split(f"/{site_name}/")
    if len(splitted) >= 2 and splitted[1]:
        return splitted[1]
    else:
        return path


@login_required
def process_getting_site(request, name, endpoint=""):

    try:
        site = Site.objects.get(name=name)
    except Site.DoesNotExist:
        raise Http404("Site does not exist")

    absolute_url = site.get_app_link_to_site(request.build_absolute_uri("/"))
    logger.info(dict(absolute_url=absolute_url, site_url=site.url))
    with Loader(absolute_url=absolute_url, site_url=site.url) as loader:
        data = loader.load(endpoint)
        Activity.objects.create(
            site=site,
            user=request.user,
            content_size=loader.total_MB,
            route=endpoint,
        )
        if not data:
            raise ValueError(f"Something went wrong {absolute_url=}{site.url=}")
        return HttpResponse(data)


@login_required
def get_site_url(request, name: str):
    return process_getting_site(request, name, endpoint="")


@login_required
def get_site_route_url(request, name: str):
    endpoint = get_site_route(site_name=name, path=request.path)
    return process_getting_site(request, name, endpoint="".join(endpoint))
