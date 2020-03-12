from django.utils import timezone


def has_expired(credentials):
    expiry_time = credentials['expiry']
    now = str(timezone.datetime.now())
    return now > expiry_time


def credentials_to_dict(credentials):
    expiry = str(credentials.expiry.utcnow())
    return {
        'access_token': credentials.token,
        'expiry': expiry
    }
