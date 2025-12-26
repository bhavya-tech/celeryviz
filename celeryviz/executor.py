import asyncio
from .event_receiver import EventListener
from .server import Server
from .data_service import get_event_sinks


def starter(ctx, record_file_path, no_socketio, port, **kwargs):
    app = ctx.obj.app
    app.control.enable_events()

    event_data_sinks = get_event_sinks(record_file_path, no_socketio, **kwargs)

    server_loop = asyncio.new_event_loop()
    server = Server(server_loop, port=port, event_data_sinks=event_data_sinks)

    event_listener = EventListener(app, server.event_handler, server_loop)
    event_listener.start()

    server.start()


