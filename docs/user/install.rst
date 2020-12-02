.. _intro:

Installation
============


Cheeseshop
----------

This part of the documentation explain to you have to integrated without changing anything
of you existing Django_ project.

Installing Bagou is simple with `pip <http://www.pip-installer.org/>`_::

    pip install django-bagou

Get source code
---------------

Has Bagou is developed on GitHub_, you can find the code `here <https://github.com/toxinu/django-bagou>`_.

Settings
--------

Add *Bagou* in your ``INSTALLED_APPS`` in ``settings.py``.
All *Bagou* settings are stored in a `Dict`` in ``settings.py``.

::

    BAGOU = {
        'DEFAULT_HANDLER_CLASS': 'bagou.handler.WebSocketHandler',
        'WEBSOCKET_URL': 'ws://localhost:9000/websocket',
        'AMQP_BROKER_URL': 'amqp://guest:guest@localhost:5672/',
        'QUEUE_NAME': 'bagou',
        'AUTH': True
    }

- ``DEFAULT_HANDLER_CLASS``: ``Class`` which dispatch all incoming messages.
- ``WEBSOCKET_URL``: URL where ``BagouWebSocket`` javascript ``Object`` will connect to.
- ``AMQP_BROKER_URL``: URL for *Pika* client to *RabbitMQ*.
- ``QUEUE_NAME``: *AMQP* queue for *Pika*.
- ``AUTH``: Enable Django authentication over websocket.

.. _Django: https://www.djangoproject.com/
.. _GitHub: https://github.com/
