Bagou: Websocket for Django
===========================

Release v\ |version|. (:ref:`Installation <install>`)

Bagou is an :ref:`MIT Licensed <mit>` Django app, written in Python.
It's support full duplex websocket.

Just create an ``events.py`` file in your app.
This will allow you to catch events.

::

    from bagou.utils import broadcast
    from bagou.events import on_message

    @on_message(channel=r"^hello$")
    def chatroom(client, channel, message):
        broadcast(
            event='message',
            channels=client.channels,
            data={'message': 'Hello World from server.'})

You can use ``broadcast`` method everywhere in your `Django` project to send message
to websocket channels.

Bagou use most of `SocketIO` concept, like subscribe, unsubscribe. Its fully compatible with
callback on websocket message.

Feature Support
---------------

- Async message sending (`with RabbitMQ`)
- Channel support (`like SocketIO`)
- Django authentification over websocket
- Enhanced ``BagouWebSocket`` javascript object
- Many event decorators (``on_subscribe``, ``on_message``, ``on_store``, ...)
- Management command for your websocket server
- Channel permissions (`soon`)

User Guide
----------

This is part of the documentation, which will start with Bagou architecture, some
websocket background information, then focuses on step-by-step instructions for your
very first Django application.

.. toctree::
  :maxdepth: 2

  user/intro
  user/install
  user/configuration
  user/authentication

API Documentation
-----------------

.. toctree::
  :maxdepth: 2

  api/events




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

