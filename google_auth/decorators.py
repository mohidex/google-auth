from django.shortcuts import redirect


def google_auth_required(function):
    def _function(request, *args, **kwargs):
        if request.session.get('credentials') is None:
            return redirect('authorize')
        return function(request, *args, **kwargs)
    return _function
