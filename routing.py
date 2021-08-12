from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/asenzor/(?P<room_name>\w+)/$', consumers.AsenzorConsumer.as_asgi()),
]