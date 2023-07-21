import os
import chat.routing

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import video.routing
from streaming.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming.settings.base')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # For regular http connection
    # 'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),  # For Websocket connection
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(
            chat.routing.websocket_urlpatterns + video.routing.websocket_urlpatterns
        ))
    ),
})
