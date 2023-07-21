from django.urls import re_path
import chat.consumers
import video.consumers
from chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", chat.consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/video_stream/(?P<room_name>\w+)/$', chat.consumers.VideoStreamConsumer.as_asgi()),
]