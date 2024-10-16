from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# If modifying these SCOPES, delete the file token.pickle
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    # Load credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def delete_social_emails():
    service = authenticate_gmail()
    # Search for emails in the Social category from LinkedIn
    query = 'category:social from:@linkedin.com'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No LinkedIn emails found in the Social category.")
        return

    # Delete the emails
    for message in messages:
        service.users().messages().delete(userId='me', id=message['id']).execute()
        print(f"Deleted email with ID: {message['id']}")

    print("All LinkedIn emails in the Social category have been deleted.")

if __name__ == '__main__':
    delete_social_emails()

