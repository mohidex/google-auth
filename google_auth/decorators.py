from django.shortcuts import redirect
from .models import GoogleAuthUser


def google_auth_required(function):
    def _function(request, *args, **kwargs):
        google_user = GoogleAuthUser.objects.filter(user=request.user).first()
        if not google_user or not google_user.refresh_token:
            return redirect('authorize')
        return function(request, *args, **kwargs)
    return _function
