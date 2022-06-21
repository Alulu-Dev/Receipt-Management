import io
from PIL import UnidentifiedImageError
from bson import ObjectId
from flask_login import current_user
from googleapiclient.http import MediaIoBaseDownload
from mongoengine import ValidationError, DoesNotExist

from API.Google import drive_service

from ..models import UserRequest, receiptDataModel, receiptItems, Categories
from .imageUploading import check_user_folder

drive = drive_service()


def display_verification_request():
    try:
        requests = UserRequest.objects()

        resolved_requests = []
        unresolved_requests = []
        for request in requests:
            if request.resolved:
                resolved_requests.append({
                    "User": request.user_id.email,
                    'Receipt': str(request.receipt_id.id),
                    'status': ['Resolved'],
                })
            else:
                unresolved_requests.append({
                    "User": request.user_id.email,
                    'Receipt': str(request.receipt_id.id),
                    'status': ['Unresolved'],
                })
        return {
            'Resolved Requests': resolved_requests,
            'Unresolved Requests': unresolved_requests
        }
    except (DoesNotExist, ValidationError):
        return "Data could be fetched", 501


def display_customers_verification_request(user):
    try:
        requests = UserRequest.objects(user_id=user)
        list_of_request = []
        for request in requests:
            data = {"receipt_id": str(request.receipt_id.id),
                    'Receipt': request.receipt_id.business_place_name,
                    'status': 'Resolved' if request.resolved else 'Unresolved'}
            list_of_request.append(data)
        return list_of_request, 200
    except DoesNotExist:
        return "Data could be fetched", 501


def create_customer_verification_request(user, receipt):
    try:
        new_request = UserRequest()
        new_request.user_id = user
        new_request.receipt_id = ObjectId(receipt)

        new_request.save()
        return 'Requested created', 201
    except ValidationError:
        return "Data could be fetched", 501


def check_receipt_verification_status(receipt):
    try:
        receiptDataModel.objects.get(id=receipt, owner=current_user.id)
        try:
            request = UserRequest.objects.get(receipt_id=receipt, user_id=current_user.id)
            return request.resolved
        except DoesNotExist:
            return "Request unsent"
    except DoesNotExist:
        return "Receipt unsent"


def get_all_receipt(user):
    receipts = receiptDataModel.objects(owner=user, deleted=False)
    list_of_receipts = []
    for receipt in receipts:
        result = get_receipt_data(receipt.id)
        list_of_receipts.append(result)

    return list_of_receipts


def get_receipt_data(receipt_id):
    receiptData = receiptDataModel.objects.get(id=receipt_id)
    list_of_items = []
    for item in receiptData.items:
        i = {
            'id': str(item.id),
            'name': item.name,
            'quantity': item.quantity,
            'price': item.item_price,
        }
        list_of_items.append(i)

    data = {
        'id': str(receiptData.id),
        'tin number': receiptData.tin_number,
        'fs number': receiptData.fs_number,
        'issued date': receiptData.issued_date.strftime("%Y-%m-%d %H:%M:%S"),
        'business place name': receiptData.business_place_name,
        'description': receiptData.description,
        "category": receiptData.category_id.category_name,
        'total price': receiptData.total_price,
        'register id': receiptData.register_id,
        'items': list_of_items,
    }
    return data


def get_receipt_image_id(username, receipt_id):
    try:
        if not check_user_folder(username):
            raise UnidentifiedImageError
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
        raise UnidentifiedImageError
    except UnidentifiedImageError:
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
        current_data = receiptDataModel.objects.get(id=ObjectId(receipt_id))

        if new_data['tin_number'] != "" and new_data['tin_number'] != current_data.tin_number:
            current_data.tin_number = new_data['tin_number']
        if new_data['fs_number'] != "" and new_data['fs_number'] != current_data.fs_number:
            current_data.fs_number = new_data['fs_number']
        if new_data['issued_date'] != "" and new_data['issued_date'] != current_data.issued_date:
            current_data.issued_date = new_data['issued_date']
        if new_data['business_place_name'] != "" and new_data[
            'business_place_name'] != current_data.business_place_name:
            current_data.business_place_name = new_data['business_place_name']
        if new_data['description'] != "" and new_data['description'] != current_data.description:
            current_data.description = new_data['description']
        if new_data['total_price'] != "" and new_data['total_price'] != current_data.total_price:
            current_data.total_price = new_data['total_price']
        if new_data['register_id'] != "" and new_data['register_id'] != current_data.register_id:
            current_data.register_id = new_data['register_id']

        current_data.save()
        return "details updated", 201
    except ValidationError:
        return "Data Couldn't Be Fetched", 500


def update_items_details_manually(item_id, new_data):
    try:
        current_data = receiptItems.objects.get(id=item_id)

        if new_data['name'] != "" and new_data['name'] != current_data.name:
            current_data.name = new_data['name']
        if new_data['quantity'] != "" and new_data['quantity'] != current_data.quantity:
            current_data.quantity = float(new_data['quantity'])
        if new_data['item_price'] != "" and new_data['item_price'] != current_data.item_price:
            current_data.item_price = float(new_data['item_price'])
        current_data.save()
        return "done", 200
    except ValidationError:
        return "Data Couldn't Be Fetched", 500
