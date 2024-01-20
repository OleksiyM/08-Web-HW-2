
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
channel.queue_declare(queue='hw_8_exchange_sms',  durable=True)
channel.queue_bind(exchange='HW_8_Exchange', queue='hw_8_exchange_sms')
channel.queue_declare(queue='hw_8_exchange_email',  durable=True)
channel.queue_bind(exchange='HW_8_Exchange', queue='hw_8_exchange_email')


def seed_contact():
    send_method = choice(PREFERRED_CONTACT_METHODS_LIST)
    new_contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        password=fake.password(length=8),
        phone=fake.phone_number(),
        born_date=fake.date_of_birth(),
        born_location=fake.city(),
        description=fake.text(),
        preferred_contact_methods=send_method,
        msg_delivered=False
    )

    return new_contact, send_method


def send_message(contact_id, send_method_via):
    message = {
        'id': str(contact_id),
        'text': f'Message {datetime.now().isoformat()}',
        'send_method': f'{send_method}'
    }
    if send_method_via == 'sms':
        channel.basic_publish(exchange='HW_8_Exchange',
                              routing_key='hw_8_exchange_sms', body=json.dumps(message).encode())
    elif send_method_via == 'email':
        channel.basic_publish(exchange='HW_8_Exchange',
                              routing_key='hw_8_exchange_email', body=json.dumps(message).encode())

    # channel.basic_publish(exchange='HW_8_Exchange',
    #                       routing_key='hw_8_exchange', body=json.dumps(message).encode())
    return f'Message sent to {contact_id} via {send_method}'


if __name__ == "__main__":
    for i in range(10):
        contact, send_method = seed_contact()
        contact.save()
        print(send_message(contact.id, send_method))

    connection.close()
