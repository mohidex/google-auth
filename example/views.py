from requests import get
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from google_auth.views import get_token

@login_required
def get_google_drive_data(requests):
    url = 'https://www.googleapis.com/drive/v3/files'
    access_token = get_token(requests)
    headers = {
        'authorization': 'Bearer ' + access_token,
        'content-type': 'application/json'
    }
    print(headers)
    res = get(url, headers=headers)
    return HttpResponse(res)
