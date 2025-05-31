from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authentication import TokenAuthentication

from ads.views import profile_view, exchange_proposals, update_exchange_status

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Barter Desk API",
        default_version='v1',
        description="Документация для обмена объявлениями и предложениями",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[TokenAuthentication],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/profile/proposals/', exchange_proposals, name='exchange_proposals_profile'),
    path('accounts/profile/proposals/<int:pk>/<str:status>/', update_exchange_status, name='update_exchange_status_profile'),
    path('api/', include('ads.api_urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
