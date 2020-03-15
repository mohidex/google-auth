from requests import get
from django.http import HttpResponse

from google_auth.views import get_token
from google_auth.decorators import google_auth_required


@google_auth_required
def google_drive(request):
    url = 'https://www.googleapis.com/drive/v3/files'
    access_token = get_token(request)
    headers = {
        'authorization': 'Bearer ' + access_token,
        'content-type': 'application/json'
    }
    res = get(url, headers=headers)
    return HttpResponse(res)
