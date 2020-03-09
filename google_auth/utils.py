import json
import requests
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from .models import GoogleAuthUser

CLIENT_SECRETS_FILE = settings.CLIENT_SECRET
with open(CLIENT_SECRETS_FILE) as f:
    secret_json = json.load(f)
client_id = secret_json['web'].get('client_id')
client_secret = secret_json['web'].get('client_secret')
token_uri = secret_json['web'].get('token_uri')


def has_expired(credentials):
    expiry_time = credentials['expiry']
    now = str(timezone.datetime.now())
    return now > expiry_time


def get_access_token(request):
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

