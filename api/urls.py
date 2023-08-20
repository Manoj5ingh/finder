from django.urls import path

from api.views import configs, gmail_connect, gmail_oauth2_callback, search

urlpatterns = [
    path('connect/gmail_auth/', gmail_connect, name='gmail_connect'),
    path('connect/oauth2callback/', gmail_oauth2_callback, name='oauth2callback'),
    path('search', search, name='search'),
    path('configs', configs, name='configs')
]