from mongoengine import DoesNotExist, ValidationError
import datetime
from ..models import receiptItems, Comparison, ItemsDictionary


def get_all_items_with_tag():
    try:
        list_of_items = []
        items = receiptItems.objects()
        for item in items:
            if item.tag is not None:
                data = {
                    'name': item.name,
                    'id': str(item.id),
                }
                list_of_items.append(data)
        return list_of_items
    except DoesNotExist:
        return "No items found", 404


def compare_items_price(item, user):
    try:
        item_tag = receiptItems.objects.get(id=item).tag

        if item_tag:
            tag = item_tag.id
            tag_name = ItemsDictionary.objects.get(id=tag).tag

            try:
                record = Comparison.objects.get(tag=tag_name, owner=user)
                today = datetime.datetime.now()
                diff = today - record.created_date
                if diff.days == 0:
                    return {"id": str(record.id)}, 200
                else:
                    raise DoesNotExist
            except DoesNotExist:

                all_items = receiptItems.objects(tag=tag)

                item_details = []
                for item in all_items:
                    data = {
                        'Shop': item.receipt_id.business_place_name,
                        'price': item.item_price / item.quantity
                    }
                    item_details.append(data)

                sorted_list = sorted(item_details, key=lambda k: k["price"])

                new_record = Comparison()
                new_record.owner = user
                new_record.tag = tag_name
                new_record.result = sorted_list[:5]

                new_record.save()

                return {"id": str(new_record.id)}, 200
        else:
            return "Item not tagged", 412
    except DoesNotExist:
        return "Data could not be fetched", 500


def all_previous_comparison(user):
    try:
        all_record = Comparison.objects(owner=user)
        list_of_record = []
        for record in all_record:
            list_of_record.append({
                'id': str(record.id),
                'tag': record.tag,
                'date': record.created_date.strftime("%Y-%m-%d %H:%M:%S")
            })

        return list_of_record
    except DoesNotExist:
        return "No report exists", 500


def previous_comparison(record_id, user):
    try:
        record = Comparison.objects.get(id=record_id, owner=user)
        data = {
            'id': str(record.id),
            'tag': record.tag,
            'date': record.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'result': record.result
        }

        return data, 200
    except DoesNotExist:
        return 'Invalid id', 400


def update_comparison(record_id, user):
    try:
        record = Comparison.objects.get(id=record_id, owner=user)
        today = datetime.datetime.now()
        diff = today - record.created_date
        if diff.days > 0:
            tag = record.tag
            item = receiptItems.objects.get(tag=tag)
            return compare_items_price(item, user)
        else:
            data = {
                'id': str(record.id),
                'tag': record.tag,
                'date': record.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'result': record.result
            }
            return data, 200
    except DoesNotExist:
        return 'Invalid id', 400


def delete_comparison(record_id, user):
    try:
        record = Comparison.objects.get(id=record_id, owner=user)
        record.delete()
        return "Deleted", 200
    except DoesNotExist:
        return "Data Doesn't Exist", 400
