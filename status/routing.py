from django.urls import re_path
from . import consumers  # You’ll need to create this too

websocket_urlpatterns = [
    re_path(r'ws/status/$', consumers.StatusConsumer.as_asgi()),
]
