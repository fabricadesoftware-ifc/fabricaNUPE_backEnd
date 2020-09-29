from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from nupe.account.router import router as account_router
from nupe.core.router import router as core_router
from nupe.core.views import custom_handler_404
from nupe.file.router import router as file_router

# quando DEBUG = False, retorna um json ao invés de renderizar um template
handler404 = custom_handler_404

# união da rota de outros apps
core_router.registry.extend(file_router.registry)
core_router.registry.extend(account_router.registry)

urlpatterns = [
    path("api/v1/", include(core_router.urls)),
    path("admin/", admin.site.urls),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# informações a serem exibidas no template do swagger
description = "Projeto realizado pela Fábrica de Software para melhorar o atendimento realizado pelo NUPE"
contact = openapi.Contact(
    name="Luis Guerreiro", url="https://linkedin.com/in/devguerreiro", email="luiscvlh11@gmail.com"
)
api_info = openapi.Info(title="Nupe API", default_version="v0.1.0", description=description, contact=contact)

schema_view = get_schema_view(info=api_info, public=True, permission_classes=[AllowAny])
