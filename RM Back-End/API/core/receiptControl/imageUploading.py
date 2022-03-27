from datetime import datetime
from googleapiclient.http import MediaFileUpload

from API.Google import drive_service
from API.settings import RECEIPT_IMAGE_STORAGE

drive = drive_service()


def check_user_folder(username):
    # check if the username has a folder
    query = f"parents='{RECEIPT_IMAGE_STORAGE}'"
    response = drive.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')
    while nextPageToken:
        response = drive.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    for folder in files:
        if folder['name'] == username:
            return folder['id']
    return False


def create_user_folder(username):
    # create user folder metadata
    folder_metadata = {
        'name': username,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [RECEIPT_IMAGE_STORAGE]
    }
    try:
        # create a folder their username
        user_folder = drive.files().create(body=folder_metadata,
                                           fields='id').execute()
    except ConnectionError:
        return False, 500
    # Get user folder ID
    user_folder_id = user_folder.get('id')
    return user_folder_id


def upload_image_to_drive(username, receipt_id, file_path, file_mimetype):
    # check if the username has a folder
    user_folder_id = check_user_folder(username)
    if not user_folder_id:
        # create user folder metadata
        user_folder_id = create_user_folder(username)
    """
    create metadata for the image
    file name format 
                "SuperAdmin 2341c3773b3e717238f04dff 2022-03-19 12:45:35"
    """
    file_metadata = {
        'name': username + ' ' + hex(receipt_id) + ' ' + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        'parents': [user_folder_id]
    }
    # create receipt image
    media_content = MediaFileUpload(file_path,
                                    mimetype=file_mimetype)
    try:
        # upload the image
        file = drive.files().create(
            body=file_metadata,
            media_body=media_content,
        ).execute()
        if file.get('id'):
            return file.get('name'), 201
    except ConnectionError:
        return False, 500
