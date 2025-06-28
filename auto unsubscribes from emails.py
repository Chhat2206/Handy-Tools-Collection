# pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client beautifulsoup4 requests

import os.path
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests

# Scopes for reading and modifying emails
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.readonly'
]


def get_unsubscribe_links(service, user_id='me'):
    """Fetch unsubscribe links from unread emails."""
    results = service.users().messages().list(userId=user_id, q="is:unread").execute()
    messages = results.get('messages', [])

    unsubscribe_links = []

    for msg in messages:
        msg_id = msg['id']
        msg = service.users().messages().get(userId=user_id, id=msg_id).execute()
        payload = msg['payload']
        headers = payload['headers']

        # Look for "List-Unsubscribe" in headers
        for header in headers:
            if header['name'].lower() == "list-unsubscribe":
                links = re.findall(r'<(https?://[^>]+)>', header['value'])
                unsubscribe_links.extend(links)

        # If "List-Unsubscribe" not found, look in the body
        if 'parts' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            soup = BeautifulSoup(body, 'html.parser')
            links = soup.find_all('a', href=True, string=re.compile(r'unsubscribe', re.I))
            unsubscribe_links.extend(link['href'] for link in links)

    return unsubscribe_links


def unsubscribe_from_links(links):
    """Visit each unsubscribe link."""
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                print(f"Successfully unsubscribed via {link}")
            else:
                print(f"Failed to unsubscribe via {link}")
        except Exception as e:
            print(f"Error visiting {link}: {e}")


def main():
    """Main function to handle authentication and unsubscribe."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        print("Fetching unsubscribe links...")
        links = get_unsubscribe_links(service)
        if links:
            print(f"Found {len(links)} unsubscribe links. Unsubscribing...")
            unsubscribe_from_links(links)
        else:
            print("No unsubscribe links found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()

