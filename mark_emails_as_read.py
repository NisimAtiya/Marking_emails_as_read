from googleapiclient.discovery import build as google_build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return google_build('gmail', 'v1', credentials=creds)

def list_unread_messages(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])
    return messages

def mark_as_read(service, message_id):
    service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()

def main():
    service = authenticate()
    unread_messages = list_unread_messages(service)
    count_marked_as_read = 0
    for message in unread_messages:
        mark_as_read(service, message['id'])
        count_marked_as_read += 1
        print(f"Marked message {message['id']} as read.")
    print(f"Total {count_marked_as_read} messages marked as read.")

if __name__ == '__main__':
    main()
