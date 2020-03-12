import json
import requests
from django.shortcuts import redirect
from django.utils import timezone
import google_auth_oauthlib.flow
from django.conf import settings
from .models import GoogleAuthUser
from django.contrib.auth.decorators import login_required
from .utils import has_expired, credentials_to_dict


CLIENT_SECRETS_FILE = settings.CLIENT_SECRET
with open(CLIENT_SECRETS_FILE) as f:
    secret_json = json.load(f)
client_id = secret_json['web'].get('client_id')
client_secret = secret_json['web'].get('client_secret')
token_uri = secret_json['web'].get('token_uri')
redirect_uri = secret_json['web'].get('redirect_uris')[0]


SCOPES = settings.SCOPES
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri)


@login_required
def get_token(request):
    user = GoogleAuthUser.objects.filter(user=request.user).first()
    if not user:
        return redirect('authorize')
    else:
        if 'credentials' in request.session and not has_expired(request.session['credentials']):
            cred = request.session['credentials']
            return cred['access_token']
        access_token, expires_in = refresh_access_token(request)
        expired_at = timezone.datetime.now() + timezone.timedelta(seconds=expires_in)
        expiry = str(expired_at)
        credentials = {
            'access_token': access_token,
            'expiry': expiry
        }
        request.session['credentials'] = credentials
        return credentials['access_token']


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


def refresh_access_token(request):
    google_user = GoogleAuthUser.objects.filter(user=request.user).first()
    if not google_user:
        return redirect('authorize')
    refresh_token = google_user.refresh_token
    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(token_uri, data=params).json()
    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    return access_token, expires_in

