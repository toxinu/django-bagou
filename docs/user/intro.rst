.. _introduction:

Introduction
============

Bagou is a Django module that help you to integrate real time websocket in an easy and flexible way in your project.

Engine is a Tornado_ WebSocket server with a Pika_ client connected on RabbitMQ_ in a asynchronous
loop.
This architecture allow you to send websocket message to channel without having
incoming message.

Incoming
--------

Incoming messages are catched by Tornado and sent to method that you can decorate.
This is a simple workflow.

::

    @on_message
    def welcome(client, channel, message):
		client.jsonify(success=True, message="Message received!")


Sending
-------

Send a message is a little more complexe.
You can send message to websocket after an incoming message, easy.

But when you want to send message in a Celery_ task, or after an SQL update
statement, you'll have to use an easy method which do all the job.

This is it.

::

    broadcast(event="message", channels="bagou", data={"message": "Welcome!"}

You can broadcast message when you want, which will internaly be publish on RabbitMQ,
consumed by Pika client. Pika which run in the same loop as Tornado, sent message to connected websockets.

Client side
-----------

A ``BagouWebSocket`` javascript Object is provided which implement almost all SocketIO_
mechanisms which I recommend you to read.

Message format
--------------

A message, from server to client or in the other way try to have a similar format. Everything is of course ``JSON``.

::

    {
        callbackId: 12345678-1234-5678-1234-567812345678,
        event: 'subscribe',
        data: {channel: 'hello'}
    }

- ``callbackId`` (*optionnal*): It's **Bagou** way to set up a bit of *Ajax* over websocket. If there is no handler or if you forward ``callbackId`` in your handlers, client will be able to do thing like that: ::

    ws.subscribe('my-channel', function(response) {
        console.log('Subscription done.');
    });

* ``event``: It's a mix of channel and typed action mechanize. For example, internal method like: ``ws.subscribe('my-channel')`` in ``BagouWebSocket`` Object, will send a message like that: ::

    {
        event: 'subscribe',
        data: {channel: 'my-channel'}
    }


Bagou License
-------------

    .. include:: ../../LICENSE


.. _Tornado: http://www.tornadoweb.org/en/stable/index.html
.. _Pika: http://pika.readthedocs.org/en/latest/
.. _RabbitMQ: http://www.rabbitmq.com/
.. _Celery: http://www.celeryproject.org/
.. _SocketIO: http://socket.io/
