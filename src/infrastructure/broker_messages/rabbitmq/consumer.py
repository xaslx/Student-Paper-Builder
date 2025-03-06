import asyncio
import aiormq
import json
from aiormq.abc import DeliveredMessage
from aiosmtplib import SMTP
from src.settings.config import Config
from email.message import EmailMessage
import logging
import smtplib

config: Config = Config()
logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, body: str):

    msg = EmailMessage()
    msg['From'] = config.smtp.smtp_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.set_content(body)

    with smtplib.SMTP_SSL(config.smtp.smtp_host, config.smtp.smtp_port) as server:
        server.login(config.smtp.smtp_user, config.smtp.smtp_pass)
        server.send_message(msg)
        
        logger.info(f'Email отправлен на {to}')


async def on_message(message: DeliveredMessage):
    try:

        email_data = json.loads(message.body.decode('utf-8'))
        logger.info(f'Получены данные для отправки email: {email_data}')


        await send_email(
            to=email_data['to'],
            subject=email_data['subject'],
            body=email_data['body']
        )


        await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag)
    except Exception as e:
        logger.error(f'Ошибка при обработке сообщения: {e}')


async def main():
    connection = await aiormq.connect(f'amqp://{config.rabbitmq.rabbitmq_user}:{config.rabbitmq.rabbitmq_password}@rabbitmq/')
    channel = await connection.channel()

    await channel.exchange_declare('main_exchange', exchange_type='direct')
    declare_ok = await channel.queue_declare('email_queue')
    await channel.queue_bind(
        queue=declare_ok.queue,
        exchange='main_exchange',
        routing_key='main_routing_key'
    )

    await channel.basic_qos(prefetch_count=1)
    await channel.basic_consume(declare_ok.queue, on_message, no_ack=False)

    logger.info('Ожидание сообщений...')
    await asyncio.Future()

# Запуск consumer
asyncio.run(main())