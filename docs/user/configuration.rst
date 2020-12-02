.. _install:

Configuration
=============

Server
------

You can handle incoming messages with methods which you'll have to decorator with appropriate
event. They are called **event handlers**.

Its very easy to handle incoming messages with **Bagou**. First thing to do is to create
``events.py`` in you application folder.

::

    from bagou.utils import broadcast
    from bagou.events import on_close
    from bagou.events import on_message
    from bagou.events import on_subscribe


    @on_message(channel=r"^hello$")
    def welcome(client, channel, message):
        broadcast(
            event='message',
            channels=client.channels,
            data={'text': 'Hello world from server.')


    @on_subscribe(channel=r"^hello$")
    def broadcast_new_user(client, channel, message):
        broadcast(
            event='message',
            channels=client.channels,
            data={'text': 'Welcome on my channel.'})


    @on_close
    def broadcast_left_user(client):
        broadcast(
            event='message',
            channels=client.channels,
            data={'text': 'Goodbye from every channel.'})

You can ``broadcast`` has many message has you want in an event. It's also possible to
just anwser to the current socket like that:

::

    client.jsonify(event='message', data={'text': 'Hey, you websocket!'})


Client
------

On the client side, you have to use ``BagouWebSocket`` which is an extended Object of ``WebSocket``.

**Bagou** give you all tools you need to set up real time events in your application.
First of all, import javascript libraries.

::

    {% load bagou_tags %}
    {% bagou_static %}

    <script type="text/javascript">
      var ws = BagouWebSocket(WEBSOCKET_URL, {
        open: function {
          console.log('Socket opened');
          ws.subscribe('bagou-channel');
        },
        events: {
          message: function(msg) {
            console.log('Receiving message');
            ws.emit('Message received');
          }
        }
      });
    </script>
