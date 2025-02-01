import aiormq
import json
from src.settings.config import Config

config: Config = Config()


async def publish(to: str, subject: str, body: str):

    connection = await aiormq.connect(f'amqp://{config.rabbitmq.rabbitmq_user}:{config.rabbitmq.rabbitmq_password}@rabbitmq/')
    channel = await connection.channel()


    await channel.exchange_declare('main_exchange', exchange_type='direct')


    email_data = {
        'to': to,
        'subject': subject,
        'body': body
    }

    await channel.basic_publish(
        body=json.dumps(email_data).encode('utf-8'),
        exchange='main_exchange',
        routing_key='main_routing_key'
    )

    await connection.close()