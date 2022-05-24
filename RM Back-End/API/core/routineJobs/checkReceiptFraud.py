import os
import time
from datetime import datetime
import schedule
from threading import Thread

from .accountRemover import account_remover_permanently
from ..fraudChecker import check_fraud
from ..receiptControl.receiptRemover import delete_receipt_permanently


def routine_manager():
    thread1 = Thread(target=threaded_task, )
    thread2 = Thread(target=threaded_task2, )
    thread3 = Thread(target=threaded_task3, )
    thread1.daemon = True
    thread2.daemon = True
    thread3.daemon = True
    thread1.start()
    thread2.start()
    thread3.start()
    return ""


def threaded_task():
    schedule.every().day.at("00:00").do(check_fraud_schedule)
    while True:
        schedule.run_pending()


def threaded_task2():
    schedule.every().day.at("00:00").do(delete_data_schedule)
    while True:
        schedule.run_pending()


def threaded_task3():
    schedule.every().day.at("00:00").do(delete_account_schedule)
    while True:
        schedule.run_pending()


def check_fraud_schedule():
    check_fraud()
    if datetime.now().hour == 6:
        return time.sleep(64800)


def delete_data_schedule():
    delete_receipt_permanently()
    if datetime.now().hour == 6:
        return time.sleep(64800)


def delete_account_schedule():
    account_remover_permanently()
    if datetime.now().hour == 6:
        return time.sleep(64800)

