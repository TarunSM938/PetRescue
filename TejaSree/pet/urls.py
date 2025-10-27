# pet/urls.py
# pet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),

    # Pet reporting pages (create these views in views.py)
    path('report-lost/', views.report_lost_pet, name='report_lost_pet'),
    path('report-found/', views.report_found_pet, name='report_found_pet'),
]



