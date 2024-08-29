from sites.models import Site, Activity
from logger import logger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.db.models import Count, Sum, Case, When, F, Q, CharField
from django.db import models
from django.db.models.functions import Concat


class ActivityList(LoginRequiredMixin, ListView):
    template_name = "activity.html"
    model = Activity
    context_object_name = "activities"

    def get_queryset(self):
        return (
            Activity.objects.filter(user=self.request.user)
            .values("site__name")
            .annotate(
                routes_count=Count("route", distinct=True),
                content_size=Sum("content_size", output_field=models.FloatField()),
                usage=Count("id"),
            )
            .values("site__name", "site__pk", "routes_count", "content_size", "usage")
        )


class SiteActivityList(LoginRequiredMixin, ListView):
    model = Site
    template_name = "partials/activity_detail.html"
    context_object_name = "activities"

    def get_context_data(self, **kwargs):
        context = super(SiteActivityList, self).get_context_data(**kwargs) # get the default context data
        context['site_name'] = self.site.values("name")[0]['name']
        return context

    def get_queryset(self):
        self.site = Site.objects.filter(creator=self.request.user, pk=self.kwargs.get('pk'))
        return (
            self.site.select_related("activity")
            .values("activity__route")
            .annotate(
                used=Count("activity__route"),
                content_size=Sum(
                    "activity__content_size", output_field=models.FloatField()
                ),
                route=Case(
                    When(
                        Q(activity__route=''), then=F('url')),
                    default=Concat(F('url'), F("activity__route"), output_field=CharField()),
                    output_field=CharField(),
                ),
            )
            .values("activity__route", "used", "content_size", "name", "route")
        )
