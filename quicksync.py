from datetime import datetime, timedelta
import os
from pprint import pprint

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'

def _in_credentials_dir(filename):
    credential_dir = 'credentials'
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    return os.path.join(credential_dir, filename)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = _in_credentials_dir('calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_synctoken():
    token_path = _in_credentials_dir('token')
    if not os.path.exists(token_path):
        return None
    with open(token_path) as f:
        token = f.read().strip()
    return token

def put_synctoken(token):
    token_path = _in_credentials_dir('token')
    print(token, file=open(token_path, 'w'))

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    service = build('calendar', 'v3', http=credentials.authorize(Http()))

    token = get_synctoken()
    if token:
        request = service.events().list(
                calendarId='primary',
                syncToken=token)
    else:
        request = service.events().list(
                calendarId='primary',
                timeMin=(datetime.utcnow() - timedelta(5)).isoformat() + 'Z' # 'Z' indicates UTC time
                )

    while True:
        result = request.execute()
        events = result.get('items', [])
        for event in events:
            pprint(event.get('summary', None))
        pageToken = result.get('nextPageToken', None)
        if not pageToken: break
    put_synctoken(result['nextSyncToken'])


if __name__ == '__main__':
    main()
