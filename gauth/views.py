from django.http import HttpResponse
from django.shortcuts import redirect
import google_auth_oauthlib.flow
from django.conf import settings


CLIENT_SECRETS_FILE = settings.CLIENT_SECRET
SCOPES = settings.SCOPES
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/oauth2callback")


def index(request):
    if request.session.get('credentials'):
        credentials = request.session.get('credentials')
        return HttpResponse(credentials.get('token'))
    else:
        return redirect('authorize')


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
    return redirect('home')


def credentials_to_dict(credentials):
    return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }