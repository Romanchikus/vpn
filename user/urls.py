from django.urls import path
from user import views
from sites import views as sites_views
from django.contrib.auth.views import LogoutView


app_name = "user"

urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("site-list/", sites_views.SiteList.as_view(), name='site-list'),
    path("add-site/", sites_views.add_site, name='add-site'),
]

hmtx_views = [
    path("check-username/", views.check_username, name="check-username"),
]

urlpatterns += hmtx_views
