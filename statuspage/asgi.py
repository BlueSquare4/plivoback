# project_root/asgi.py
import os
from django.core.asgi import get_asgi_application
import socketio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statuspage.settings")

# Standard Django ASGI app
django_asgi_app = get_asgi_application()

# Create a Socket.IO server instance.
# The async_mode "asgi" makes it work in the ASGI context.
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
# Mount the Socket.IO server on top of the Django app.
application = socketio.ASGIApp(sio, django_asgi_app)

# Define Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print("Socket.IO: Client connected:", sid)
    # Automatically add the client to the "status_updates" room
    await sio.enter_room(sid, "status_updates")

@sio.event
async def disconnect(sid):
    print("Socket.IO: Client disconnected:", sid)
