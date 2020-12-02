.. _events:

Events
======

All events which doesn't have any handler and have a *callbackId* are automatically
forwared to websocket.

..  py:decorator::   bagou.events.on_open

    Fired when a new client open a socket

    Passed arguments: ``client``, ``callback``

..  py:decorator::   bagou.events.on_close

    Fired when a client close its socket

    Passed arguments: ``client``, ``callback``

..  py:decorator::   bagou.events.on_store

    Fired when a client set data in its store

    Passed arguments: ``client``, ``channel``, ``message``, ``callback``

..  py:decorator::   bagou.events.on_authenticate

    Fired when a client authenticate in Django backend

    Passed arguments: ``client``, ``sessionid``, ``callback``

..  py:decorator::   bagou.events.on_subscribe(channel)

    Fired when a client subscribe to a channel

    Passed arguments: ``client``, ``channel``, ``message``, ``callback``

..  py:decorator::   bagou.events.on_unsubscribe(channel)

    Fired when a client unsubscribe to a channel

    Passed arguments: ``client``, ``channel``, ``message``, ``callback``

..  py:decorator::   bagou.events.on_message(channel)

    Fired when a client send a message

    Passed arguments: ``client``, ``channel``, ``message``, ``callback``

..  py:decorator::   bagou.events.on_callback(channel)

    Fired when a client ask for a callback

    Passed arguments: ``client``, ``channel``, ``message``, ``callback``
