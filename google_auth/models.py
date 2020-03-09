from django.db import models
from django.contrib.auth.models import User


class GoogleAuthUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='token_of'
    )
    refresh_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
