import json
from django.shortcuts import redirect
import google_auth_oauthlib.flow
from django.conf import settings
from django.http import JsonResponse
from .models import GoogleAuthUser
from .utils import get_access_token
from django.contrib.auth.decorators import login_required


CLIENT_SECRETS_FILE = settings.CLIENT_SECRET
with open(CLIENT_SECRETS_FILE) as f:
    secret_json = json.load(f)


SCOPES = settings.SCOPES
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=secret_json['web'].get('redirect_uris')[0])


@login_required
def get_token(request):
    user = GoogleAuthUser.objects.filter(user=request.user).first()
    if not user:
        return redirect('authorize')
    else:
        get_access_token(request)
        cred = request.session['credentials']
        access_token = cred.get('access_token')
        return JsonResponse({'access_token': access_token})


def authorize(request):
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
        )

    # Store the state so the callback can verify the auth server response.
    request.session['state'] = state

    return redirect(authorization_url)


def oauth2callback(request):
    state = request.session['state']

    flow.state = state
    code = request.GET.get('code', False)
    flow.fetch_token(code=code)
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    google_auth, created = GoogleAuthUser.objects.get_or_create(user=request.user)
    google_auth.refresh_token = credentials.refresh_token
    google_auth.save()
    return redirect('token')


def credentials_to_dict(credentials):
    expiry = str(credentials.expiry.utcnow())
    return {
        'access_token': credentials.token,
        'expiry': expiry
    }

