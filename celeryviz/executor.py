import asyncio
from .event_receiver import EventListener
from .server import Server
from .data_service import get_event_sinks
from .config import settings

def starter(ctx):
    app = ctx.obj.app
    app.control.enable_events()

    event_data_sinks = get_event_sinks()

    server_loop = asyncio.new_event_loop()
    server = Server(server_loop, port=settings.port, event_data_sinks=event_data_sinks)

    event_listener = EventListener(app, server.event_handler, server_loop)
    event_listener.start()

    server.start()


