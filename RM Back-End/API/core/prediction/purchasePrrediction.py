import datetime
from sklearn import svm
from ..models import receiptDataModel, receiptItems


def get_user_items(user):
    # try:
    user_receipts = receiptDataModel.objects(owner=user)
    list_of_items = []
    for receipt in user_receipts:
        day = receipt.issued_date.day
        month = receipt.issued_date.month
        year = receipt.issued_date.year

        items = receiptItems.objects(receipt_id=receipt.id)
        for item in items:
            name = item.name
            quantity = item.quantity
            list_of_items.append([name, quantity, day, month, year])
    return list_of_items


def group_items_with_same_date_and_name(items):
    result_list = []
    for item in items:
        flag = False
        for result in result_list:
            if item[0] == result[0] and item[2] == result[2] and item[3] == result[3] and item[4] == result[4]:
                result[1] = result[1] + item[1]
                flag = True
        if not flag:
            result_list.append(item)

    return result_list


def group_purchase_by_week(dataset):
    weekly_purchase = []
    i = 0
    for entry in dataset:
        week_flag = False
        year = int(entry[4])
        month = int(entry[3])
        day = int(entry[2])
        week_number = datetime.date(year, month, day).isocalendar().week

        if len(weekly_purchase) == 0:
            weekly_purchase.append({
                'year': year,
                "week_no": week_number,
                'items': [
                    {
                        "name": entry[0],
                        "quantity": int(entry[1])
                    }
                ]
            })
        else:
            for purchase in weekly_purchase:
                item_found = False
                match = (purchase['year'] ==
                         year and purchase['week_no'] == week_number)

                if match:
                    week_flag = True
                    for item in purchase['items']:
                        if entry[0] == item['name']:
                            item_found = True
                            item["quantity"] = item["quantity"] + int(entry[1])
                            break
                    if not item_found:
                        purchase['items'].append({
                            "name": entry[0],
                            "quantity": int(entry[1])
                        })
                    break

            if not week_flag:
                weekly_purchase.append({
                    'year': year,
                    "week_no": week_number,
                    'items': [
                        {
                            "name": entry[0],
                            "quantity": int(entry[1])
                        }
                    ]
                })

    return weekly_purchase


def weekly_purchase_dict_to_list(list_of_dictionary):
    list_of_data = []
    for dictionary in list_of_dictionary:
        for item in dictionary['items']:
            temp = [item['name'], item['quantity'],
                    dictionary['week_no'], dictionary['year']]

            list_of_data.append(temp)

    return list_of_data


def predict(data):
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_week = datetime.date(current_date.year, current_date.month, current_date.day).isocalendar().week
    next_week = current_week + 1
    predictions = {}
    X = []
    y = []

    for item, quantity, week, year in data:
        for i in range(int(quantity)):
            X.append([year, week])
            y.append(item)

    clf = svm.SVC(probability=True)
    clf.fit(X, y)

    test = [
        [year, week]
        for year in [current_year]
        for week in [next_week]
    ]
    prediction = clf.predict_proba(test)
    for (year, week), proba in zip(test, prediction):
        data = [{"item": cls, "probability": "{:.2f}".format(p * 100)}
                for cls, p in zip(clf.classes_, proba)]
        predictions = {
            "year": year,
            "week_no": week,
            "items": data
        }
    return predictions


def get_prediction(user):
    user_previous_purchase_history_items = get_user_items(user)
    stage1_preprocessed_data = group_items_with_same_date_and_name(user_previous_purchase_history_items)
    stage2_preprocessed_data = group_purchase_by_week(stage1_preprocessed_data)
    data_set = weekly_purchase_dict_to_list(stage2_preprocessed_data)
    predictions = predict(data_set)
    sorted_prediction = sorted(predictions['items'], key=lambda d: d['probability'], reverse=True)

    top_5_predictions = {
        "year": predictions["year"],
        "week_no": predictions["week_no"],
        'items': sorted_prediction[:5]
    }

    return top_5_predictions
