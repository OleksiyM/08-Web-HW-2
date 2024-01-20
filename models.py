from bson import json_util
from mongoengine import connect, Document, StringField, BooleanField, DateField, DateTimeField, ListField, ReferenceField, CASCADE

import os

from dotenv import load_dotenv

import pika
from pika.exceptions import AMQPConnectionError

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

PREFERRED_CONTACT_METHODS_LIST = ['email', 'phone']

URI = f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority'

# uri = "mongodb+srv://<username>:<password>@cluster0.vhirvg8.mongodb.net/?retryWrites=true&w=majority"

connect(db='Web-HW-8-2', host=URI)


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True,  min_length=8)
    born_date = DateField()
    born_location = StringField()
    description = StringField()
    msg_delivered = BooleanField(default=False)







