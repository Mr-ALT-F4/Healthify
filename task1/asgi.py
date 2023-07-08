"""
ASGI config for task1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task1.settings')

from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
asgiapplication = get_asgi_application()
from .routing import ws_pattern

application=ProtocolTypeRouter(
    {
        "http": asgiapplication,
        'websocket':AuthMiddlewareStack(URLRouter(ws_pattern)),
    }
)
