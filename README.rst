Bagou
=====

Tornado WebSocket server backed with PikaClient connected on RabbitMQ.

The goal of this architecture is to provide a way to integrate full duplex websockets in
synchronous application with RabbitMQ as message bus.

Server is Tornado WebSocketHandler with a PikaClient consumer.

Installation
------------

::

    git clone https://github.com/toxinu/django-bagou.git
    cd django-bagou/example
    virtualenv virtenv
    source virtenv/source/activate
    pip install django
    pip install -e ..
    python manage.py runserver
    # In another terminal
    python manage.py runwebsocket
    # Go to http://localhost:8000


Incoming
--------
For example, incoming websocket messages from Tornado are pushed to a queue (Celery for example)
or just computed.

 * Browser send websocket message
 * Tornado received it
   * Sending AMQP message
   * Run Celery task (from Django?)
 * Torndo reply to websocket
 * Browser received websocket message

Sending
-------
Django application can publish messages on RabbitMQ, which will be consumed by Pika and
pushed to websockets.

 * Running arbitary Python code
 * Send AMQP message to websocket queue
 * PikaClient wich run with Tornado consumed it
 * PikaClient tell Tornado to send websocket message to browser
 * Browser received websocket message


Todo
----

 * Channel permission
 * User authentification based on sessionid
 * Integrated with Celery ?
 * Helpers for getting channels
