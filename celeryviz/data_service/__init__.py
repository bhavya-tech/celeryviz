from .base import AbstractEventSink, AbstractEventRetriever
from .file_event_sink import FileEventSink
from .socketio_event_sink import SocketioEventSink


from ..config import settings

def get_event_sinks():
    data_sinks = []
    
    if settings.record_file:
        file_sink = FileEventSink(settings.record_file)
        data_sinks.append(file_sink)

    if not settings.no_socketio:
        socketio_sink = SocketioEventSink()
        data_sinks.append(socketio_sink)

    return data_sinks


__all__ = ["FileEventSink", "SocketioEventSink", "get_event_sinks", "AbstractEventSink",
           "AbstractEventRetriever"]