# -*- coding: utf-8 -*-
import uuid

from .exceptions import BagouChannelException


class Channel(object):
    def __init__(self, name=None, owner=None, allow_anonymous=True, persistent=False):
        self.name = name
        if name is None:
            self.name = str(uuid.uuid4())

        self.clients = [owner]
        self.allowed_clients = []
        self.max_client = None
        self.allow_anonymous = allow_anonymous
        self.owner = owner
        self.persistent = persistent

    def add_client(self, client):
        if client.user.is_anonymous() and not self.allow_anonymous:
            raise BagouChannelException("Anonymous users not allowed.")
        if self.allowed_clients:
            if client not in self.allowed_clients:
                raise BagouChannelException("Client not in allowed_clients.")
        if self.max_client is not None and len(self.clients) + 1 > self.max_client:
            raise BagouChannelException("Channel is full.")

        if client not in self.clients:
            self.clients.append(client)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
