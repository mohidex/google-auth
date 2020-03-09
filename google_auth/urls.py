from django.urls import path
from .views import get_token, authorize, oauth2callback

urlpatterns = [
    path('token/', get_token, name='token'),
    path('authorize/', authorize, name='authorize'),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
]
