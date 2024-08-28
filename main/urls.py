from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from sites.urls import urlpatterns as sites_urls

urlpatterns = [
    # TODO: provide access to an admin page
    path("admin/", admin.site.urls),
    # TODO: provide access to an user page
    path("user/", include("user.urls")),
    path("", include("sites.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
