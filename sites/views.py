from django.shortcuts import render

from django.http import HttpResponse

from sites.loader import Loader


def test(request):
    url = "https://zaxid.net/koli_varto_peresadzhuvati_fikus_i_yak_tse_pravilno_robiti_poradi_n1586438"
    with Loader() as loader:
        return HttpResponse(loader.load(url))
