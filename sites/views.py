from typing import Optional, Union

from django.http import Http404, HttpResponse

from sites.loader import Loader
from sites.models import Site, Activity
from django.shortcuts import redirect


def test(request):
    url = "https://zaxid.net/koli_varto_peresadzhuvati_fikus_i_yak_tse_pravilno_robiti_poradi_n1586438"
    with Loader() as loader:
        return HttpResponse(loader.load(url))


def get_site_route(site_name: str, path: str) -> Union[list[str], bool]:
    splitted: list[str] = path.split(f"/{site_name}/")
    if len(splitted) >= 2 and splitted[1]:
        return splitted[1:]
    else:
        return path


def process_getting_site(request, name, endpoint=[""]):

    try:
        site = Site.objects.get(name=name)
    except Site.DoesNotExist:
        raise Http404("Site does not exist")

    absolute_url = site.get_app_link_to_site(request.build_absolute_uri("/"))
    print(dict(absolute_url=absolute_url, site_url=site.url))
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


def get_site_url(request, name: str):
    return process_getting_site(request, name, endpoint="")


def get_site_route_url(request, name: str):
    endpoint = get_site_route(site_name=name, path=request.path)
    return process_getting_site(request, name, endpoint=endpoint)
