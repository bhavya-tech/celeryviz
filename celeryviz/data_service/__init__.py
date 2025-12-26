from .base import AbstractEventSink, AbstractEventRetriever
from .file_event_sink import FileEventSink
from .socketio_event_sink import SocketioEventSink
from .clickhose_datasource import ClickhouseSink


def get_event_sinks(record_file_path, no_socketio, **kwargs):
    data_sinks = []
    
    if record_file_path:
        file_sink = FileEventSink(record_file_path)
        data_sinks.append(file_sink)

    if not no_socketio:
        socketio_sink = SocketioEventSink()
        data_sinks.append(socketio_sink)


    if kwargs.get("clickhouse_enable"):
        clickhouse_config = {key: kwargs.get(key) for key in ClickhouseSink.config_options}
        clickhouse_sink = ClickhouseSink(clickhouse_config)
        data_sinks.append(clickhouse_sink)

    return data_sinks


__all__ = ["FileEventSink", "SocketioEventSink", "get_event_sinks", "AbstractEventSink",
           "AbstractEventRetriever"]