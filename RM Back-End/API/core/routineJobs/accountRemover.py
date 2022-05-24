from datetime import datetime

from mongoengine import DoesNotExist

from ..models import (accountModel, receiptDataModel)


def account_remover_permanently():
    try:
        today = datetime.today()
        accounts = accountModel.objects(delete=True)
        try:
            for account in accounts:
                day = account.data_created
                delta = today - day
                if delta.days > 30:
                    receipts = receiptDataModel.objects(owner=account.id)
                    for receipt in receipts:
                        receipt.deleted = True
                    account.delete()
        except Exception as e:
            return "Routine Account Removal Failed!\n" + str(e)
    except DoesNotExist:
        pass
