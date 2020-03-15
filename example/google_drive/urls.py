from django.contrib import admin
from django.urls import path, include
from .views import google_drive
urlpatterns = [
    path('', google_drive),
    path('admin/', admin.site.urls),
    path('google-auth/', include('google_auth.urls'), name='google-authentication'),
]
