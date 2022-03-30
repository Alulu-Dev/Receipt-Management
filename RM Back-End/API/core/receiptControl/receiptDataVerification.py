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

