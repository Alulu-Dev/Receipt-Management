from mongoengine import DoesNotExist, ValidationError

from ..models import receiptItems, Comparison, ItemsDictionary


def compare_items_price(item, user):
    try:
        item_tag = receiptItems.objects.get(id=item).tag

        if item_tag:
            tag = item_tag.id
            tag_name = ItemsDictionary.objects.get(id=tag).tag
            all_items = receiptItems.objects(tag=tag)

            item_details = []
            for item in all_items:
                data = {
                    'Shop': item.receipt_id.business_place_name,
                    'price': item.item_price / item.quantity
                }
                item_details.append(data)

            sorted_list = sorted(item_details, key=lambda k: k["price"])

            record = Comparison()
            record.owner = user
            record.tag = tag_name
            record.result = sorted_list[:5]

            record.save()

            return sorted_list[:5]
        else:
            return "Item not tagged"
    except DoesNotExist:
        return "Data could not be fetched", 500


def all_previous_comparison(user):
    try:
        all_record = Comparison.objects(owner=user)
        list_of_record = []
        for record in all_record:
            list_of_record.append({
                'tag': record.tag,
                'date': record.created_date.strftime("%Y-%m-%d %H:%M:%S")
            })

        return list_of_record
    except DoesNotExist:
        return "No report exists", 500


def previous_comparison(record_id):
    try:
        record = Comparison.objects.get(id=record_id)
        data = {
                'tag': record.tag,
                'date': record.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'result': record.result
            }

        return data
    except:
        return 'Invalid id', 400
