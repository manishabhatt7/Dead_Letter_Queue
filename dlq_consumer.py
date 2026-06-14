import json

from rabbitmq import get_connection
from config import DLQ_QUEUE

connection = get_connection()
channel = connection.channel()



def callback(ch, method, properties, body):

    message = json.loads(body)

    print('\n========= DLQ MESSAGE =========')
    print(json.dumps(message, indent=2))
    print('===============================')

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=DLQ_QUEUE,
    on_message_callback=callback
)

print('DLQ consumer listening...')

channel.start_consuming()