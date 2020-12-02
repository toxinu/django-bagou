.. _configuration:

Authentication
==============

Django-bagou provide Django session authentication over Websocket.

To enable it you have to set ``AUTH = True`` in Bagou configuration.

Server
------

You can access User_ object associated to a websocket with ``user`` attribut.

::

    @on_open
    def welcome_user(client)
        client.jsonify(message="Hi, %s" % client.user.get_full_name())

Client
------

You have total control of when you want to authenticate a websocket.

::

    var ws = BagouWebSocket(WEBSOCKET_URL, {
      open: function { ws.auth(); }
    }

You can not authenticate a websocket without using ``sessionid``.

.. _User: https://docs.djangoproject.com/en/dev/ref/contrib/auth/#user
