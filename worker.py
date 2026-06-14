import json
import random

from rabbitmq import get_connection
from config import (
    MAIN_QUEUE,
    RETRY_QUEUE,
    MAX_RETRIES,
)

connection = get_connection()
channel = connection.channel()


channel.basic_qos(prefetch_count=1)


def process_email(email: str):

    # Simulate random failure
    if random.randint(1, 10) < 7:
        raise Exception('SMTP server failed')

    print(f'Email sent to {email}')



def callback(ch, method, properties, body):

    message = json.loads(body)

    try:

        email = message['payload']['email']

        print('\nProcessing message')
        print(message)

        process_email(email)

        print('SUCCESS')

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:

        print(f'FAILED: {e}')

        retry_count = message.get('retry_count', 0)

        if retry_count >= MAX_RETRIES:

            print('Sending to DLQ')

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )

        else:

            message['retry_count'] = retry_count + 1

            print(f'Retrying: {message["retry_count"]}')

            channel.basic_publish(
                exchange='',
                routing_key=RETRY_QUEUE,
                body=json.dumps(message)
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=MAIN_QUEUE,
    on_message_callback=callback
)

print('Worker waiting for messages...')

channel.start_consuming()