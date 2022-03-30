import io
from googleapiclient.http import MediaIoBaseDownload
from mongoengine import ValidationError

from API.Google import drive_service

from ..models import UserRequest, receiptDataModel, receiptItems
from .imageUploading import check_user_folder

drive = drive_service()


def display_verification_request():
    try:
        requests = UserRequest.objects()

        resolved_requests = []
        unresolved_requests = []
        for request in requests:
            if request.request_resolved:
                resolved_requests.append({
                    "User": request.user_id,
                    'Receipt': request.receipt_id,
                    'status': 'Resolved',
                })
            else:
                unresolved_requests.append({
                    "User": request.user_id,
                    'Receipt': request.receipt_id,
                    'status': 'Unresolved',
                })
        return {
            'Resolved Requests': resolved_requests,
            'Unresolved Requests': unresolved_requests
        }
    except ValidationError:
        return "Data could be fetched", 501


def display_customers_verification_request(user):
    try:
        requests = UserRequest.objects.get(user_id=user)

        return ({"User": x.user_id,
                 'Receipt': x.receipt_id,
                 'status': 'Resolved' if x.request_resolved else 'Unresolved'}
                for x in requests)
    except ValidationError:
        return "Data could be fetched", 501


def create_customer_verification_request(user, receipt):
    try:
        new_request = UserRequest()
        new_request.user_id = user
        new_request.receipt_id = receipt

        new_request.save()
        return new_request.id, 201
    except ValidationError:
        return "Data could be fetched", 501


def get_receipt_data(receipt_id):
    receiptData = receiptDataModel.objects.get(id=receipt_id)
    list_of_items = []
    for item in receiptData.items:
        i = {
            'name ': item.name,
            'quantity ': item.quantity,
            'price': item.item_price,
        }
        list_of_items.append(i)

    data = {
        'tin number': receiptData.tin_number,
        'fs number': receiptData.fs_number,
        'issued date': receiptData.issued_date.strftime("%Y-%m-%d %H:%M:%S"),
        'business place name': receiptData.business_place_name,
        'description': receiptData.description,
        'total price': receiptData.total_price,
        'register id': receiptData.register_id,
        'items': list_of_items,
    }
    return data


def get_receipt_image_id(username, receipt_id):
    try:
        if not check_user_folder(username):
            raise ConnectionError
        parent_uid = check_user_folder(username)
        # check for the receipt image
        query = f"parents='{parent_uid}'"
        response = drive.files().list(q=query).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')
        while nextPageToken:
            response = drive.files().list(q=query).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        for file in files:
            if receipt_id in file['name']:
                # return file['id']
                return download_receipt_image(file_id=file['id'])
        raise ConnectionError
    except ConnectionError:
        return "Image could not fetched"


def download_receipt_image(file_id):
    try:
        request = drive.files().get_media(fileId=file_id,
                                          )
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        return file
    except ConnectionError:
        return "Download failed"


def update_receipt_details_manually(receipt_id, new_data):
    try:
        current_data = receiptDataModel.objects.get(id=receipt_id)

        if 'tin_number' in new_data and new_data['tin_number'] != current_data.tin_number:
            current_data.tin_number = new_data['tin_number']
        if 'fs_number' in new_data and new_data['fs_number'] != current_data.fs_number:
            current_data.fs_number = new_data['fs_number']
        if 'issued_date' in new_data and new_data['issued_date'] != current_data.issued_data:
            current_data.issued_data = new_data['issued_date']
        if 'business_place_name' in new_data and new_data['business_place_name'] != current_data.business_place_name:
            current_data.business_place_name = new_data['business_place_name']
        if 'description' in new_data and new_data['description'] != current_data.description:
            current_data.description = new_data['description']
        if 'total_price' in new_data and new_data['total_price'] != current_data.total_price:
            current_data.total_price = new_data['total_price']
        if 'register_id' in new_data and new_data['register_id'] != current_data.register_id:
            current_data.register_id = new_data['register_id']

        current_data.save()
    except ValidationError:
        return "Data Couldn't Be Fetched", 500

def update_items_details_manually(receipt_id, new_data):
    try:
        current_data = receiptItems.objects.get(id=receipt_id)

        if 'name' in new_data and new_data['name'] != current_data.name:
            current_data.name = new_data['name']
        if 'quantity' in new_data and new_data['quantity'] != current_data.quantity:
            current_data.quantity = new_data['quantity']
        if 'item_price' in new_data and new_data['item_price'] != current_data.item_price:
            current_data.item_price = new_data['item_price']
        current_data.save()
    except ValidationError:
        return "Data Couldn't Be Fetched", 500