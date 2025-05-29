from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('create/', views.ad_create, name='ad_create'),
    path('<int:pk>/edit/', views.ad_update, name='ad_update'),
    path('<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='ad_list'), name='logout'),
    path('ads/<int:ad_id>/propose/', views.create_exchange_proposal, name='create_exchange_proposal'),
]
