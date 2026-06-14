import json

from fastapi import FastAPI

from rabbitmq import get_connection, setup_queues
from config import MAIN_QUEUE
from schemas import create_message

app = FastAPI()

setup_queues()


@app.post('/send')
def send_message(email: str):

    message = create_message(
        task_type='send_email',
        payload={
            'email': email
        }
    )

    connection = get_connection()
    channel = connection.channel()

    channel.basic_publish(
        exchange='',
        routing_key=MAIN_QUEUE,
        body=message.model_dump_json(),
        properties=None
    )

    connection.close()

    return {
        'message': 'Task queued',
        'event_id': message.event_id
    }