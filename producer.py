
import pika
import json
from datetime import datetime
from faker import Faker
from models import Contact, PREFERRED_CONTACT_METHODS_LIST
from random import choice

fake = Faker()

# RabbitNQ connection
credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW_8_Exchange', exchange_type='direct')
channel.queue_declare(queue='hw_8_exchange',  durable=True)
channel.queue_bind(exchange='HW_8_Exchange', queue='hw_8_exchange')


def seed_contact():
    new_contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        password=fake.password(length=8),
        born_date=fake.date_of_birth(),
        born_location=fake.city(),
        description=fake.text(),
        msg_delivered=False
    )

    return new_contact


def send_message(contact_id):
    message = {
        'id': str(contact_id),
        'text': f'Message {datetime.now().isoformat()}'
    }
    channel.basic_publish(exchange='HW_8_Exchange',
                          routing_key='hw_8_exchange', body=json.dumps(message).encode())
    return f'Message sent to {contact_id}'


if __name__ == "__main__":
    for i in range(10):
        contact = seed_contact()
        contact.save()
        print(send_message(contact.id))

    connection.close()
