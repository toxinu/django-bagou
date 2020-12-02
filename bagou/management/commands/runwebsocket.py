# -*- coding: utf-8 -*-
import re
import sys
import socket
from datetime import datetime
from optparse import make_option
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.conf import settings

from bagou import __version__
from bagou.server import WebSocketServer


naiveip_re = re.compile(r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
):)?(?P<port>\d+)$""", re.X)
DEFAULT_PORT = settings.BAGOU['WEBSOCKET_PORT']
DEFAULT_ADDR = settings.BAGOU['WEBSOCKET_ADDR']


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--ipv6',
            '-6',
            action='store_true',
            dest='use_ipv6',
            default=False,
            help='Tells Tornado to use a IPv6 address.'),)
    help = "Run Tornado server with Pika Client"
    args = '[optional port number, or ipaddr:port]'

    def handle(self, addrport='', *args, **options):
        self.use_ipv6 = options.get('use_ipv6')
        if self.use_ipv6 and not socket.has_ipv6:
            raise CommandError('Your Python does not support IPv6.')
        if args:
            raise CommandError('Usage is runwebsocket %s' % self.args)
        self._raw_ipv6 = False
        if not addrport:
            self.addr = ''
            self.port = DEFAULT_PORT
        else:
            m = re.match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError("%r is not a valid port number." % self.port)
            if self.addr:
                if _ipv6:
                    self.addr = self.addr[1:-1]
                    self.use_ipv6 = True
                    self._raw_ipv6 = True
                elif self.use_ipv6 and not _fqdn:
                    raise CommandError('"%s" is not a valid IPv6 address.' % self.addr)
        if not self.addr:
            self.addr = '::1' if self.use_ipv6 else DEFAULT_ADDR
            self._raw_ipv6 = bool(self.use_ipv6)

        settings.BAGOU['WEBSOCKET_PORT'] = self.port
        settings.BAGOU['WEBSOCKET_ADDR'] = self.addr
        self.run(*args, **options)

    def run(self, *args, **options):
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'
        self.stdout.write((
            "%(started_at)s\n"
            "Bagou version %(version)s, using settings %(settings)r\n"
            "Starting development server at http://%(addr)s:%(port)s/\n"
            "Consuming on %(amqp_url)s (queue: %(queue_name)s)\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            "started_at": datetime.now().strftime('%B %d, %Y - %X'),
            "version": __version__,
            "settings": settings.SETTINGS_MODULE,
            "addr": '[%s]' % self.addr if self._raw_ipv6 else self.addr,
            "amqp_url": settings.BAGOU.get('AMQP_BROKER_URL'),
            "queue_name": settings.BAGOU.get('QUEUE_NAME'),
            "port": self.port,

            "quit_command": quit_command,
        })
        websocket_server = WebSocketServer()
        websocket_server.run()
