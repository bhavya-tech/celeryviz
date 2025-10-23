import asyncio

from .event_receiver import EventListener
from .server import Server


def starter(ctx, record, file, port):  # <-- Add 'port' here
    app = ctx.obj.app

    app.control.enable_events()

    server_loop = asyncio.get_event_loop()
    # Pass the 'port' to the Server constructor
    server = Server(server_loop, record=record, file=file, port=port)

    event_listener = EventListener(app, server.event_handler, server_loop)
    event_listener.start()

    # The server.start() method will now use the port
    # it received during initialization.
    server.start()
