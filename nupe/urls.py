from django.contrib import admin
from django.urls import include, path

from nupe.core.router import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path(r"oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]
