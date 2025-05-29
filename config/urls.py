from django.contrib import admin
from django.urls import path, include
from ads.views import profile_view, exchange_proposals, update_exchange_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('accounts/profile/proposals/', exchange_proposals, name='exchange_proposals_profile'),
    path('accounts/profile/proposals/<int:pk>/<str:status>/', update_exchange_status, name='update_exchange_status_profile'),
    path('accounts/profile/', profile_view, name='profile'),
]
