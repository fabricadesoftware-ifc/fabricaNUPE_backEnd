from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from nupe.core.router import router as core_router
from nupe.core.views import custom_handler_404
from nupe.file.router import router as file_router
from project import description, developer_email, developer_name, developer_social_url

# quando DEBUG = False, retorna um json ao invés de renderizar um template
handler404 = custom_handler_404

# informações a serem exibidas no template do swagger
contact = openapi.Contact(name=developer_name, url=developer_social_url, email=developer_email)
api_info = openapi.Info(title="Nupe API", default_version="v1", description=description, contact=contact)

schema_view = get_schema_view(info=api_info, public=True, permission_classes=[AllowAny])

core_router.registry.extend(file_router.registry)  # união da rota de outros apps

urlpatterns = [
    path("api/v1/", include(core_router.urls)),
    # path("api/v1/token/", TokenObtainPairView.as_view(), name="token"),
    # path("api/v1/refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    path("admin/", admin.site.urls),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("endpoints/", schema_view.with_ui(renderer="swagger"), name="endpoints"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
