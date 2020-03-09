from django.contrib import admin
from .models import GoogleAuthUser


class GoogleAuthUserOption(admin.ModelAdmin):
    """GoogleAuthUser options"""
    list_display = ('user', 'refresh_token')
    search_fields = ('user',)


admin.site.register(GoogleAuthUser, GoogleAuthUserOption)
