## DjGoogleAuth

A google auth authenticator backend for django. This backend will generate a google access token to access and manipulate google private data(i.e. google analytics, googlemybusiness, or personal data).

### Installation
```bash
pip install git+https://github.com/msi007/google-auth.git
```

Add google_auth to your INSTALLED_APPS

```python
INSTALLED_APPS = (
    ...
    'google_auth',
)
```

Include auth urls to your urls.py

```python
urlpatterns = patterns(
    ...
    path('google-auth/', include('google_auth.urls'), name='google-authentication'),
)
```

### Settings

Add client_secret.json file path and scopes which you want access

Example: 
```python
CLIENT_SECRET = os.path.join(BASE_DIR, 'client_secrets.json')

# Add your scopes here
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly'
    ]
```

### Migrate the database

```bash
python manage.py makemigrations
python manage.py migrate
```

## Usage:

Use `@google_auth_required` decorator in all view function where you need the access token.

Example:

```python
from requests import get
from django.http import HttpResponse

from google_auth.views import get_token
from google_auth.decorators import google_auth_required


@google_auth_required
def get_google_drive_data(request):
    url = 'https://www.googleapis.com/drive/v3/files'
    access_token = get_token(request)
    headers = {
        'authorization': 'Bearer ' + access_token,
        'content-type': 'application/json'
    }
    res = get(url, headers=headers)
    return HttpResponse(res)

```
