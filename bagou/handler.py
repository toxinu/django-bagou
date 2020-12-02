# -*- coding: utf-8 -*-
import json
import logging
import tornado.websocket

from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session

from .events import on_open
from .events import on_close
from .events import on_store
from .events import on_message
from .events import on_subscribe
from .events import on_unsubscribe
from .events import on_authenticate

from .channel import Channel

logging.basicConfig()
logger = logging.getLogger("tornado.handler")
logger.setLevel(logging.INFO)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        self.channels = {}
        self.user = AnonymousUser()

        self.store = {}

        self.application.pika_client.add_event_listener(self)

        on_open.send(self)
        logger.info("WebSocket opened")

    def on_close(self):
        logger.info("WebSocket closed")
        self.application.pika_client.remove_event_listener(self)
        on_close.send(self)

    def _on_authenticate(self, message):
        session_id = None
        data = {}

        cookies = self.request.headers.get('Cookie')
        if cookies:
            logger.info('Cookies: ' + cookies);
            for cookie in cookies.split(';'):
                if cookie.strip().startswith('sessionid='):
                    session_id = cookie.split('=')[1].strip()
                    break

        if session_id:
            data = {}
            try:
                session = Session.objects.get(session_key=session_id)
                uid = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(pk=uid)
                if user:
                    self.user = user
                    self.authenticated = True
                    logger.info('User authenticated')

                    user_json = serializers.serialize('json', [self.user])[0]
                    data.update({'user': user_json})
                else:
                    logger.info('User failed to authenticate.')
            except (Session.DoesNotExist, User.DoesNotExist):
                logger.warning('User send bad sessionid.')

            self.jsonify(
                event='callback',
                data=data,
                callbackId=message.get('callbackId'))
            on_authenticate.send(self, session_id)

    def _on_subscribe(self, message):
        channel_name = message.get('data', {}).get('channel')
        callback_id = message.get('callbackId')
        if channel_name:
            logger.info("Subscribing to '%s' channel." % channel_name)
            if channel_name not in self.application.channels:
                channel = Channel(name=channel_name, owner=self)
                self.application.channels[channel_name] = channel
            else:
                channel = self.application.channels[channel_name]
                self.application.channels[channel_name].add_client(self)

            self.channels[channel_name] = channel

            logger.info('Calling on_subscribe event handlers')
            on_subscribe.send(self, message, channel, callback_id)

    def _on_unsubscribe(self, message):
        channel_name = message.get('data', {}).get('channel')
        callback_id = message.get('callbackId')
        if channel_name:
            logger.info("Unsubscribing to '%s' channel." % channel_name)
            if channel_name in self.application.channels:
                channel = self.application.channels[channel_name]
                if self in channel.clients:
                    channel.remove_client(self)
                    del self.channels[channel_name]

                    if not channel.client and not self.persistent:
                        del self.application.channels[channel_name]

                logger.info('Calling on_unsubscribe event handlers')
                on_unsubscribe.send(self, message, channel, callback_id)

    def _on_store(self, message):
        callback_id = message.get('callbackId')
        self.store.update(message.get('data'))
        on_store.send(self, message, callback_id)

    def on_message(self, message):
        logger.info("Message received: %s " % message)

        message_json = json.loads(message)
        if not isinstance(message_json, dict):
            self.jsonify(event="error", data={'message': 'bad message format'})

        message_event = message_json.get('event')
        if message_event == 'subscribe':
            self._on_subscribe(message_json)
        elif message_event == 'unsubscribe':
            self._on_unsubscribe(message_json)
        elif message_event == 'store':
            self._on_store(message_json)
        elif message_event == 'authenticate':
            self._on_authenticate(message_json)
        else:
            logger.info('Calling on_message event handlers')
            on_message.send(self, message_json)

    def jsonify(self, **kwargs):
        self.write_message(kwargs)
