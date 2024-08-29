from django.urls import path
from user import views
from sites.views import sites as sites_views
from sites.views import activity as activity_views
from django.contrib.auth.views import LogoutView


app_name = "user"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("site-list/", sites_views.SiteList.as_view(), name="site-list"),
    path("add-site/", sites_views.SiteCreate.as_view(), name="add-site"),
    path("activity/", activity_views.ActivityList.as_view(), name="activity"),
    path(
        "activity/<int:pk>/",
        activity_views.SiteActivityList.as_view(),
        name="activity-site",
    ),
]
