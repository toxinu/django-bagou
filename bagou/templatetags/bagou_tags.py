# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("bagou_scripts.html", takes_context=True)
def bagou_static(context):
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['STATIC_URL'] = settings.STATIC_URL
    context['WEBSOCKET_URL'] = settings.BAGOU.get('WEBSOCKET_URL')
    return context
