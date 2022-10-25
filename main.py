import os
from typing import Union

import google.auth

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_sa_to_impersonate() -> Union[str, None]:
    return os.getenv("SA_TO_IMPERSONATE", None)

# Ask to ADC to obtain an access token with a scope expected by the API
# (see more -> https://developers.google.com/drive/api/v3/reference/files/list#auth)
target_scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
credentials, _ = google.auth.default(scopes=target_scopes)

if get_sa_to_impersonate():
    from google.auth import impersonated_credentials
    credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=get_sa_to_impersonate(),
        target_scopes=target_scopes
    )

service = build('drive', 'v3', credentials=credentials)

def main():
    try:
        # Call the Drive v3 API 
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return

        print("Please find below each file:")
        for item in items:
            print("filename: {}".format(item['name']))
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == "__main__":
   main()