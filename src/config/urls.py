from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/sellers/", include("apps.sellers.urls")),
    path("api/v1/catalog/", include("apps.catalog.urls")),
    path("api/v1/channels/", include("apps.channels.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    path("api/v1/logistics/", include("apps.logistics.urls")),

    # Webhooks externos (sin autenticación JWT, usan firma HMAC)
    path("api/v1/sync-engine/", include("apps.sync_engine.urls")),
    path("webhooks/", include("apps.webhooks.urls")),

    # Documentación API (solo en dev o con flag)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Health check (para ALB y ECS)
    path("health/", include("apps.core.health_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
