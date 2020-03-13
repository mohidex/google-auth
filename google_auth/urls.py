from django.urls import path
from .views import authorize, oauth2callback

urlpatterns = [
    path('authorize/', authorize, name='authorize'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
]
