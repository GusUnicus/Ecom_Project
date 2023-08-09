import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('Keys/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Keys/mail_token.json', SCOPES)
            creds = flow.run_local_server(port=0)
   
        with open('Keys/token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def list_drafts():
    gmail_service = get_gmail_service()
    results = gmail_service.users().drafts().list(userId='ecommercesecured@gmail.com').execute()
    drafts = results.get('drafts', [])
    if not drafts:
        print('No drafts found.')
    else:
        print('Drafts:')
        for draft,count in zip(drafts,len(drafts)):
            print(count,draft)

def create_draft():
    gmail_service = get_gmail_service()
    subject = "Test Draft"
    body = "This is a test draft."
    sender_email = "sender@example.com"
    recipient_email = "recipient@example.com"

    message = f"From: {sender_email}\nTo: {recipient_email}\nSubject: {subject}\n\n{body}"
    raw_message = base64.urlsafe_b64encode(message.encode()).decode()
    draft = {'message': {'raw': raw_message}}
    draft = gmail_service.users().drafts().create(userId='ecommercesecured@gmail.com', body=draft).execute()
    print('Draft created:', draft['id'])

def send_email(recipient_email, subject, body):
    sender_email = 'ecommercesecured@gmail.com'
    gmail_service = get_gmail_service()
    message = f"From: {sender_email}\nTo: {recipient_email}\nSubject: {subject}\n\n{body}"
    raw_message = base64.urlsafe_b64encode(message.encode()).decode()

    email_body = {'raw': raw_message}
    sent_email = gmail_service.users().messages().send(userId=sender_email, body=email_body).execute()
    


