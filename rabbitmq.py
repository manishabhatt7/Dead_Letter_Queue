import pika

from config import (
    RABBITMQ_HOST,
    MAIN_QUEUE,
    RETRY_QUEUE,
    DLQ_QUEUE,
    DLX_EXCHANGE,
    RETRY_EXCHANGE,
)


def get_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )


def setup_queues():
    connection = get_connection()
    channel = connection.channel()

    # Dead Letter Exchange
    channel.exchange_declare(
        exchange=DLX_EXCHANGE,
        exchange_type='direct'
    )

    # Retry Exchange
    channel.exchange_declare(
        exchange=RETRY_EXCHANGE,
        exchange_type='direct'
    )

    # DLQ
    channel.queue_declare(queue=DLQ_QUEUE, durable=True)

    channel.queue_bind(
        exchange=DLX_EXCHANGE,
        queue=DLQ_QUEUE,
        routing_key='dead'
    )

    # Main Queue
    main_args = {
        'x-dead-letter-exchange': DLX_EXCHANGE,
        'x-dead-letter-routing-key': 'dead'
    }

    channel.queue_declare(
        queue=MAIN_QUEUE,
        durable=True,
        arguments=main_args
    )

    # Retry Queue
    retry_args = {
        'x-message-ttl': 5000,
        'x-dead-letter-exchange': '',
        'x-dead-letter-routing-key': MAIN_QUEUE
    }

    channel.queue_declare(
        queue=RETRY_QUEUE,
        durable=True,
        arguments=retry_args
    )

    connection.close()