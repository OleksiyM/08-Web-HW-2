import pika
import sys
import os
import time
import json
from models import Contact, connect
from bson.objectid import ObjectId


def main():
    # RabbitNQ connection
    credentials = pika.PlainCredentials('guest', 'guest')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hw_8_exchange_sms', durable=True)

    def send_message(contact_id, send_method):
        print(f'Sending message to the user ...')
        time.sleep(0.5)
        return (f'Message was sent via {send_method}')

    def callback(ch, method, properties, body):

        message = json.loads(body.decode())
        _id = message.get('id')
        send_method_via = message.get('send_method')
        send_method = message.get('send_method')
        print(f'Ready to send message: {message}')

        contact = Contact.objects(id=_id).first()
        print(send_message(_id, send_method))
        contact.update(msg_delivered=True)
        contact.save()
        print(f'Completed task #{method.delivery_tag}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hw_8_exchange_sms', on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
