from django.contrib import admin
from django.urls import path
from .views import index, authorize, oauth2callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('authorize/', authorize, name='authorize'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
]
