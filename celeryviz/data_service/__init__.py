from .file_event_sink import FileEventSink
from .socketio_event_sink import SocketioEventSink


def get_event_sinks(record_file_path, no_socketio):
    data_sinks = []
    
    if record_file_path:
        file_sink = FileEventSink(record_file_path)
        data_sinks.append(file_sink)

    if not no_socketio:
        socketio_sink = SocketioEventSink()
        data_sinks.append(socketio_sink)

    return data_sinks
