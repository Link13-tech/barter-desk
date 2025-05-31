from django.urls import path
from . import api_views
from .auth_views import CustomAuthToken, LogoutAPIView

urlpatterns = [
    path('auth/login/', CustomAuthToken.as_view(), name='api_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('ads/', api_views.AdListCreateAPIView.as_view(), name='api_ad_list_create'),
    path('ads/<int:pk>/', api_views.AdRetrieveUpdateDestroyAPIView.as_view(), name='api_ad_detail'),
    path('proposals/', api_views.ExchangeProposalListAPIView.as_view(), name='api_proposal_list'),
    path('proposals/create/', api_views.ExchangeProposalCreateAPIView.as_view(), name='api_proposal_create'),
    path('proposals/<int:pk>/update-status/', api_views.ExchangeProposalUpdateStatusAPIView.as_view(), name='api_proposal_update'),
]
