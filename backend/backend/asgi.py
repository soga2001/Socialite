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
from django.urls import re_path
django.setup()
from comments.consumers import SpillConsumer, CommentConsumer
from users.consumers import UserConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        # "websocket": AuthMiddlewareStack(
        #     URLRouter(
        #         comments.urls.websocket_urlpatterns
        #     )
        # ),
        "websocket": URLRouter([
            re_path(r'^ws/spill/(?P<post_id>[0-9a-f-]+)/$', SpillConsumer.as_asgi()),
            re_path(r'^ws/comment/(?P<comment_id>\d+)/$', CommentConsumer.as_asgi()),
            re_path(r'^ws/user_consumer/(?P<username>\w+)/$', UserConsumer.as_asgi()),
        ])
        # Just HTTP for now. (We can add other protocols later.)

})