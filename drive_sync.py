import os
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
DB_FILE = 'attendance_system.db'
GDRIVE_FILE_NAME = 'attendance_system.db'  # Google Drive name

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_to_drive(service):
    # Check if the file already exists in Drive
    results = service.files().list(q=f"name='{GDRIVE_FILE_NAME}'", fields="files(id, name)").execute()
    items = results.get('files', [])
    file_metadata = {'name': GDRIVE_FILE_NAME}
    media = MediaFileUpload(DB_FILE, resumable=True)

    if items:
        # File exists, update it
        file_id = items[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print("✔️ Database updated in Google Drive.")
    else:
        # File doesn't exist, create it
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("📤 Database uploaded to Google Drive.")

def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    print("🔁 Starting real-time sync every 1 minute...")
    while True:
        if os.path.exists(DB_FILE):
            upload_to_drive(service)
        else:
            print(f"❌ File not found: {DB_FILE}")
        time.sleep(60)  # every 1 minute

if __name__ == '__main__':
    main()
