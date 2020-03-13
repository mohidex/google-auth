from django.shortcuts import redirect
from .models import GoogleAuthUser
from django.contrib.auth.decorators import login_required


def google_auth_required(function):
    @login_required
    def _function(request, *args, **kwargs):
        google_user = GoogleAuthUser.objects.filter(user=request.user).first()
        if not google_user or not google_user.refresh_token:
            return redirect('authorize')
        return function(request, *args, **kwargs)
    return _function
