

from django.contrib import admin
from django.urls import path, include
from home.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('pets/', include('pets.urls')),
]
    



