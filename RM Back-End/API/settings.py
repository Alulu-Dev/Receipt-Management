import os

MONGO_URI = os.environ.get('MONGO_URI')
ALULU_APP_MONGO_DATABASE = os.environ.get('ALULU_APP_MONGO_DATABASE')

CLIENT_SECRET_FILE = os.environ.get('CLIENT_SECRET_FILE')

API_NAME = os.environ.get('API_NAME')

API_VERSION = os.environ.get('API_VERSION')

SCOPES = [os.environ.get('SCOPES')]

RECEIPT_IMAGE_STORAGE = os.environ.get('RECEIPT_IMAGE_STORAGE')

APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")
