import asyncio
from .event_receiver import EventListener
from .server import Server

def starter(ctx, record, file, port):
    app = ctx.obj.app
    app.control.enable_events()

    server_loop = asyncio.get_event_loop()
    server = Server(server_loop, record=record, file=file, port=port)

    event_listener = EventListener(app, server.event_handler, server_loop)
    event_listener.start()

    server.start()
