"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
django.setup()
import comments.urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        # "websocket": AuthMiddlewareStack(
        #     URLRouter(
        #         comments.urls.websocket_urlpatterns
        #     )
        # ),
        "websocket": URLRouter(comments.urls.websocket_urlpatterns)
        # Just HTTP for now. (We can add other protocols later.)

})