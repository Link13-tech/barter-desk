from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('create/', views.ad_create, name='ad_create'),
    path('<int:pk>/edit/', views.ad_update, name='ad_update'),
    path('<int:pk>/delete/', views.ad_delete, name='ad_delete'),
]
