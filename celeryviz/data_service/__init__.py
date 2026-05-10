from .base import AbstractEventSink, AbstractEventRetriever
from .file_event_sink import FileEventSink
from .socketio_event_sink import SocketioEventSink
from .clickhose_datasource import ClickhouseSink, ClickhouseRetriever, ClickhouseConfig


from ..config import settings

def get_event_sinks():
    data_sinks = []
    
    if settings.record_file:
        file_sink = FileEventSink(settings.record_file)
        data_sinks.append(file_sink)

    if not settings.no_socketio:
        socketio_sink = SocketioEventSink()
        data_sinks.append(socketio_sink)

    if ClickhouseConfig.is_enabled(settings.as_dict()):
        clickhouse_config = ClickhouseConfig(settings.as_dict())
        clickhouse_sink = ClickhouseSink(clickhouse_config)
        data_sinks.append(clickhouse_sink)

    return data_sinks


def get_event_retrievers(**kwargs):
    data_retrievers = []

    if ClickhouseConfig.is_enabled(kwargs):
        clickhouse_config = ClickhouseConfig(kwargs)
        clickhouse_retriever = ClickhouseRetriever(clickhouse_config)
        data_retrievers.append(clickhouse_retriever)

    return data_retrievers


__all__ = ["FileEventSink", "SocketioEventSink", "get_event_sinks", "AbstractEventSink",
           "AbstractEventRetriever", "get_event_retrievers"]