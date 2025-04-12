# status/utils.py
from asgiref.sync import async_to_sync
from statuspage.asgi import sio  # Adjust the import path as needed

def notify_clients(data):
    # Emit a "status_update" event with the given data to all clients in the room "status_updates"
    async_to_sync(sio.emit)("status_update", data, room="status_updates")
