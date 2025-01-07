import os
import google_drive
import dropbox
import onedrive

def upload_to_cloud(storage_service, file_path):
    if storage_service == 'google_drive':
        google_drive.upload_file(file_path)
    elif storage_service == 'dropbox':
        dropbox.upload_file(file_path)
    elif storage_service == 'onedrive':
        onedrive.upload_file(file_path)