import json

from rabbitmq import get_connection
from config import MAIN_QUEUE

connection = get_connection()
channel = connection.channel()


failed_message = {
    "event_id": "manual-replay",
    "task_type": "send_email",
    "payload": {
        "email": "replayed@gmail.com"
    },
    "retry_count": 0
}

channel.basic_publish(
    exchange='',
    routing_key=MAIN_QUEUE,
    body=json.dumps(failed_message)
)

print('Message replayed')

connection.close()