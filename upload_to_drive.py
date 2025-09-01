import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define scopes (limited access)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def upload_db_to_drive(file_path, drive_filename):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': drive_filename,
        'mimeType': 'application/x-sqlite3',
        'parents': ['root']  # Upload to Drive root (or specify a folder ID)
    }

    media = MediaFileUpload(file_path, mimetype='application/x-sqlite3')
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"File uploaded! ID: {file.get('id')}")

# Example: Upload SQLite DB
upload_db_to_drive('attendance_system.db', 'backup_attendance.db')