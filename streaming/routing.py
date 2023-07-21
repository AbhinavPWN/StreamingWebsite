from django.urls import re_path, path
from streams import consumer

websocket_urlpatterns = [
    # re_path(r'ws/stream/(?P<stream_name\d+)/$', consumer.StreamConsumer.as_asgi()),
    # path('ws/stream/<int:stream_id>/', consumer.StreamConsumer.as_asgi()),
]

