from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google-auth/', include('google_auth.urls'), name='google-authentication'),
]
