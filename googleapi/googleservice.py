import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def create_service():
    client_secret_file = 'googleapi/google_photos_client.json'
    api_name = 'photoslibrary'
    api_version = 'v1'
    scopes = ['https://www.googleapis.com/auth/photoslibrary']
    pickle_file = f'googleapi/token_{api_name}_{api_version}.pickle'
    cred = None

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file,
                scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(
            api_name,
            api_version,
            credentials=cred,
            static_discovery=False)
        return service
    except Exception as e:
        print(e)
    return None
