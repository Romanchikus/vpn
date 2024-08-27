from typing import Optional, Union

from django.http import Http404, HttpResponse

from sites.loader import Loader
from sites.models import Site, Activity
from django.shortcuts import redirect


def test(request):
    url = "https://zaxid.net/koli_varto_peresadzhuvati_fikus_i_yak_tse_pravilno_robiti_poradi_n1586438"
    with Loader() as loader:
        return HttpResponse(loader.load(url))


def get_base_site_url(request, name):
    try:
        s = Site.objects.get(name=name)
    except Site.DoesNotExist:
        raise Http404("Site does not exist")
    with Loader() as loader:
        return HttpResponse(loader.load(s.url))


def get_site_route(
    request, site: Site, orig_url: Optional[str]
) -> Union[None, str, bool]:
    if not orig_url:
        return None
    splitted: list[str] = orig_url.split(site.url)
    if len(splitted) >= 2:
        return splitted[1]
    else:
        return False


def get_site_url(request, name):
    orig_url: str = request.GET.get("orig_url")
    try:
        site = Site.objects.get(name=name)
    except Site.DoesNotExist:
        raise Http404("Site does not exist")

    endpoint = get_site_route(request, site, orig_url)
    if endpoint is False:
        redirect(orig_url)

    absolute_url = site.get_app_link_to_site(request.build_absolute_uri("/"))
    with Loader(absolute_url=absolute_url) as loader:
        data = loader.load(orig_url)
        Activity.objects.create(
            site=site,
            user=request.user,
            content_size=0,
            route=endpoint,
        )
        return HttpResponse(data)
