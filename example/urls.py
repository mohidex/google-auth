from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import get_google_drive_data

urlpatterns = [
    path('', get_google_drive_data),
    path('admin/', admin.site.urls),
    path('google-auth/', include('google_auth.urls'), name='google-authentication'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
