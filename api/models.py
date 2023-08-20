import requests
from django.contrib.auth.models import User
from django.db import models

from finder import settings


class GmailOAuthToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)

    def is_expired(self):
        from datetime import datetime
        return self.token_expiry < datetime.now()

    def get_access_token(self):
        if not self.is_expired():
            return self.access_token

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET
        }

        response = requests.post(settings.GOOGLE_TOKEN_URI, data=payload)

        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data.get('access_token')
            self.access_token = access_token
            self.save()
            return access_token
        else:
            print("Error fetching access token:", response.status_code, response.text)
            return None