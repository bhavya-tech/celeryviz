import asyncio
from .event_receiver import EventListener
from .server import Server
from .data_service import FileEventSink, SocketioEventSink


def starter(ctx, record_file_path, no_socketio, port):
    app = ctx.obj.app
    app.control.enable_events()

    event_data_sinks = get_event_sinks(record_file_path, no_socketio)

    server_loop = asyncio.new_event_loop()
    server = Server(server_loop, port=port, event_data_sinks=event_data_sinks)

    event_listener = EventListener(app, server.event_handler, server_loop)
    event_listener.start()

    server.start()


def get_event_sinks(record_file_path, no_socketio):
    data_sinks = []
    
    if record_file_path:
        file_sink = FileEventSink(record_file_path)
        data_sinks.append(file_sink)

    if not no_socketio:
        socketio_sink = SocketioEventSink()
        data_sinks.append(socketio_sink)

    return data_sinks
