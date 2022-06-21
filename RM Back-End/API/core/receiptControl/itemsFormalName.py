from bson import ObjectId
from mongoengine import DoesNotExist
from urllib3.exceptions import ResponseError

from ..models import receiptItems, ItemsDictionary


def create_formal_name(name):
    try:
        tag = ItemsDictionary.objects.get(tag=name)
        return str(tag.id)
    except DoesNotExist:
        new_tag = ItemsDictionary()
        new_tag.tag = name
        new_tag.save()

        return str(new_tag.id)


def add_formal_name_to_items(tag_id, item_id):
    try:
        item = receiptItems.objects.get(id=ObjectId(item_id))
        tag_id = ObjectId(tag_id)

        if ItemsDictionary.objects.get(id=tag_id):
            item.update(set__tag=tag_id)
            return 'Ok'
    except ResponseError:
        return "Operation failed", 501


def remove_formal_name_to_items(tag_id, item_id):
    try:
        item = receiptItems.objects.get(id=ObjectId(item_id))
        tag_id = ObjectId(tag_id)

        if ItemsDictionary.objects.get(id=tag_id):
            item.update(set__tag=None)
            return "Removed", 201
    except ResponseError:
        return "Operation failed", 501


def partial_match(list_of_items):
    partially_matched_items = []
    for item in list_of_items:
        if list_of_items in item.name:
            partially_matched_items.append({
                'name': item.name,
                'id': item.id,
                'owner': item.owner_id
            })
    return partially_matched_items


def tags_match(list_of_items, item_tag):
    tags_matched_items = []
    for item in list_of_items:
        if item_tag == item.tag:
            tags_matched_items.append({
                'name': item.name,
                'id': item.id,
                'owner': item.owner_id
            })
    return tags_matched_items


def search_items_for_system(item_name, search_type='both'):
    """
    :return a combination of 2 lists one with the partial name matches
            and the other with tags matches
    """
    try:
        item_tag = receiptItems.objects.get(name=item_name).tag
        items_list = receiptItems.objects()

        partially_matched_items = partial_match(items_list)
        tags_matched_items = tags_match(items_list, item_tag)

        if search_type == 'partial':
            result = partially_matched_items
        elif search_type == 'tags':
            result = tags_matched_items
        else:
            result = list(set(partially_matched_items + tags_matched_items))

        return result
    except ResponseError:
        return "Data could not be found", 404


def search_items_for_user(item_name, owner_id):
    try:
        results = search_items_for_system(item_name)

        list_of_items = []
        for item in results:
            if item['owner'] == owner_id:
                list_of_items.append(item)

        return list_of_items
    except ResponseError:
        return "No Items found", 404


def get_all_items():
    try:
        items = receiptItems.objects()
        list_of_items = []
        for item in items:
            try:
                item_tag = item.tag.tag
                tag_id = str(item.tag.id)
            except AttributeError:
                item_tag = None
                tag_id = None

            list_of_items.append({"id": str(item.id), "name": item.name, "tag": item_tag, "tag_id": tag_id})
        return {"items": list_of_items}, 200
    except:
        return "Oops Something went wrong", 500


def get_all_tags():
    try:
        items = ItemsDictionary.objects()
        list_of_items = []
        for item in items:
            list_of_items.append({"id": str(item.id), "name": item.tag})
        return {"tags": list_of_items}, 200
    except:
        return "Oops Something went wrong", 500
