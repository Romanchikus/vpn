from typing import Union

from django.http import Http404, HttpResponse
from django.shortcuts import render

from sites.forms import CreateSiteForm
from sites.loader import Loader
from sites.models import Site, Activity
from logger import logger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from sites.views.utils import get_site_route, process_getting_site


class SiteList(LoginRequiredMixin, ListView):
    template_name = "sites.html"
    model = Site
    context_object_name = "sites"

    def get_queryset(self):
        return Site.objects.filter(creator=self.request.user)


class SiteCreate(LoginRequiredMixin, CreateView):
    form_class = CreateSiteForm
    template_name = "create_site.html"
    success_url = reverse_lazy("user:site-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

@login_required
def get_site_url(request, name: str):
    return process_getting_site(request, name, endpoint="")


@login_required
def get_site_route_url(request, name: str):
    endpoint = get_site_route(site_name=name, path=request.path)
    return process_getting_site(request, name, endpoint="".join(endpoint))
