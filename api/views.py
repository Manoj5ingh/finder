from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import traceback

from api.models import GmailOAuthToken
from api.search.utils import search_text
from finder import settings
from users.models import CustomUser


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def gmail_connect(request):
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                    "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
                    "auth_uri": settings.GOOGLE_AUTH_URI,
                    "token_uri": settings.GOOGLE_TOKEN_URI,
                }
            },
            scopes=['https://www.googleapis.com/auth/gmail.readonly'],
            redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI,
        )
        custom_state = request.user.id
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            prompt='consent',
            state=custom_state,
        )
        return Response({'redirectUrl': authorization_url}, status=status.HTTP_200_OK)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('GET',))
def gmail_oauth2_callback(request):
    try:
        user_id = request.GET.get('state')
        if not user_id:
            raise Exception("User not found")
        else:
            user_id = int(user_id)
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                    "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
                    "auth_uri": settings.GOOGLE_AUTH_URI,
                    "token_uri": settings.GOOGLE_TOKEN_URI,
                }
            },
            state=request.GET.get('state'),
            redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI,
            scopes=['https://www.googleapis.com/auth/gmail.readonly'],
        )

        flow.fetch_token(authorization_response=settings.BASE_URL + request.get_full_path())
        creds = flow.credentials
        oauth = GmailOAuthToken(
            user_id=user_id,
            refresh_token=creds.refresh_token,
            token_expiry=creds.expiry
        )
        oauth.save()
        user = CustomUser.objects.get(id=user_id)
        user.add_search_method("gmail")
        return redirect(settings.BASE_URL)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(('GET',))
def search(request):
    try:
        query = request.query_params.get('query')
        user = request.user
        search_methods = user.get_search_methods()
        results = search_text(user.id, query, search_methods)
        return Response(results, status=status.HTTP_200_OK)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
@api_view(('GET',))
def configs(request):
    try:
        user = request.user
        return Response(user.get_search_methods(), status=status.HTTP_200_OK)
    except Exception as e:
        traceback.print_exc()
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
