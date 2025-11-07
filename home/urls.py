from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),              # Home page
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),


    path('api/login/', views.api_login, name='api-login'),
]
