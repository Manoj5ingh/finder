from .base_search import BaseSearch
from api.models import GmailOAuthToken
from finder import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from users.models import CustomUser


class GmailSearch(BaseSearch):
    def search(self, user_id, query):
        service = self.__get_gmail_service(user_id)
        msgs = self.__list_gmail_messages(service=service, query=query, user_id=user_id)
        return msgs

    def __get_gmail_service(self, user_id):
        auth_creds = GmailOAuthToken.objects.get(user_id=user_id)
        creds = Credentials(
            None,
            client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            refresh_token=auth_creds.refresh_token,
            token_uri=settings.GOOGLE_TOKEN_URI,
        )
        return build('gmail', 'v1', credentials=creds)

    def __list_gmail_messages(self, service, query, user_id, max_results=5):
        results = []
        user = CustomUser.objects.get(id=user_id)
        result = service.users().messages().list(userId=user.email, q=query, maxResults=max_results).execute()
        messages = result.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(userId=user.email, id=message['id']).execute()
            results.append(
                {"snippet": msg.get('snippet', 'No snippet available'),
                 "target_url": self.__generate_gmail_url(message['id'])}
            )
        return results

    def __generate_gmail_url(self, message_id):
        base_url = "https://mail.google.com/mail/u/0/#inbox/"
        return f"{base_url}{message_id}"
