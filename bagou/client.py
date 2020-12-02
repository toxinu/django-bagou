# -*- coding: utf-8 -*-
import pika
import json
import logging

from django.conf import settings

from pika.adapters.tornado_connection import TornadoConnection

logger = logging.getLogger("pika")
logger.setLevel(logging.INFO)


class PikaClient(object):

    def __init__(self, io_loop):
        logger.info('Initializing')
        self.io_loop = io_loop

        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None

        self.event_listeners = set([])

    def connect(self):
        if self.connecting:
            logger.info('Already connecting to RabbitMQ')
            return

        logger.info('Connecting to RabbitMQ')
        self.connecting = True

        cred = pika.PlainCredentials(
            settings.BAGOU.get('AMQP_BROKER_USER'),
            settings.BAGOU.get('AMQP_BROKER_PASS'))
        param = pika.ConnectionParameters(
            host=settings.BAGOU.get('AMQP_BROKER_ADDR'),
            port=settings.BAGOU.get('AMQP_BROKER_PORT'),
            virtual_host=settings.BAGOU.get('AMQP_BROKER_PATH'),
            credentials=cred)

        self.connection = TornadoConnection(param, on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        logger.info('Connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        logger.info('Channel open, Declaring exchange')
        self.channel = channel
        self.channel.queue_declare(
            queue=settings.BAGOU.get('QUEUE_NAME'),
            durable=True,
            exclusive=False,
            auto_delete=True,
            callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        self.channel.basic_consume(self.on_message, queue=settings.BAGOU.get('QUEUE_NAME'))

    def on_closed(self, connection):
        logger.info('RabbitMQ connection closed')
        self.io_loop.stop()

    def on_message(self, channel, method, header, body):
        logger.debug('Message received: %s' % body)
        self.notify_listeners(body)

    def notify_listeners(self, event_obj):
        event_json = json.loads(event_obj)
        channels = event_json.get('channel')

        for channel in channels:
            for listener in self.event_listeners:
                if channel:
                    if channel in listener.channels:
                        listener.write_message(event_obj)
                        logger.info('Notified %s (channels: %s)' % (repr(listener), listener.channels))
                else:
                    listener.write_message(event_obj)
                    logger.info('Notified %s' % repr(listener))

    def add_event_listener(self, listener):
        self.event_listeners.add(listener)
        logger.info('Listener %s added' % repr(listener))

    def remove_event_listener(self, listener):
        try:
            self.event_listeners.remove(listener)
            logger.info('Listener %s removed' % repr(listener))
        except KeyError:
            pass
