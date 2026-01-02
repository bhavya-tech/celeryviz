import asyncio
from datetime import datetime
from uuid import UUID
from typing import Any, List, Sequence
from celeryviz.data_service.base import AbstractConfigurableService, AbstractEventSink, AbstractEventRetriever
from clickhouse_connect import get_client as clickhouse_get_client
import logging

try:
    import chdb
except ImportError:
    chdb = None

logger = logging.getLogger(__name__)


class ClickhouseConfig(AbstractConfigurableService):

    config_options = ('clickhouse_host', 'clickhouse_port', 'clickhouse_database',
                     'clickhouse_username', 'clickhouse_password', 'clickhouse_engine',
                     'clickhouse_enable', 'clickhouse_file_path')
    
    @staticmethod
    def is_enabled(config: dict) -> bool:
        return config.get("clickhouse_enable", False)
    
    def __init__(self, config: dict):
        self.config = config

        if not 'clickhouse_engine' in config:
            raise ValueError("clickhouse_engine must be specified.")

        if self.engine in ('Memory', 'File') and chdb is None:
            raise ImportError("chdb library is required for ClickHouse in-memory engine. Please using pip install celeryviz[chdb].")
        
        if self.engine == 'File' and not config.get("clickhouse_file_path"):
            raise ValueError("clickhouse_file_path must be provided when using File engine.")
        
        if self.engine == 'MergeTree':
            required_fields = ('clickhouse_host', 'clickhouse_port',
                               'clickhouse_database')
            missing_fields = [field for field in required_fields if field not in config or config[field] is None]

            if missing_fields:
                raise ValueError(f"Missing required ClickHouse configuration fields for MergeTree engine: {', '.join(missing_fields)}")

    def get_connection_config(self) -> dict:

        if self.engine == 'MergeTree':
            return {
                "host": self.config.get("clickhouse_host"),
                "port": self.config.get("clickhouse_port", 8123),
                "username": self.config.get("clickhouse_username"),
                "password": self.config.get("clickhouse_password", ""),
                "database": self.config.get("clickhouse_database", "default")
            }
        else:
            return {'path': self.config.get("clickhouse_file_path", None)}
    
    @property
    def engine(self) -> str:
        return self.config.get("clickhouse_engine", "Memory")


class ClickhouseSink(AbstractEventSink):
    """Clickhouse implementation of the AbstractEventSink."""

    def __init__(self, clickhouse_config: ClickhouseConfig):
        logger.info("Initializing ClickhouseSink")

        self.client = _get_client(clickhouse_config)

        engine = clickhouse_config.engine
        _ClickhouseHelpers.create_tables(self.client, engine=engine)

    async def dump_events(self, events: List[dict]):
        """Insert a list of event dictionaries into Clickhouse."""
        rows = _ClickhouseHelpers.convert_json_to_clickhouse_format(events)
        await self.client.insert("task_events", rows)


class ClickhouseRetriever(AbstractEventRetriever):
    """Clickhouse implementation of the AbstractEventRetriever."""

    url_endpoint_name = "clickhouse"

    def __init__(self, clickhouse_config: ClickhouseConfig):
        logger.info("Initializing ClickhouseRetriever")

        self.client = _HostedClickhouseClient(
            **clickhouse_config.get_connection_config()
        )

    async def fetch_events(self, start_time: datetime, end_time: datetime) -> List[dict]:
        """Retrieve events from Clickhouse within the specified time range."""

        def _convert_datetime_to_clickhouse_format(dt: datetime) -> str:
            return f"'{dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}'"

        query = f"""
        SELECT event_time, task_id, event_type, hostname, payload
        FROM task_events
        WHERE event_time >= {(_convert_datetime_to_clickhouse_format(start_time))}
          AND event_time <= {(_convert_datetime_to_clickhouse_format(end_time))}
        ORDER BY event_time ASC
        """

        result = await _HostedClickhouseClient.query(self.client, query)

        events = _ClickhouseHelpers.convert_clickhouse_to_json_format(result)
        return events
    
    async def head_method(self):
        """Handle HEAD requests for event data."""
        return {'status': 'OK', 'detail': 'ClickhouseRetriever is available.'}


class _AbstractClickhouseClient:
    """Base Clickhouse client interface."""

    def execute(self, query: str):
        raise NotImplementedError


class _HostedClickhouseClient(_AbstractClickhouseClient):
    def __init__(self, host=None, port=8123, username=None, password="", database="default"):
        self.client = clickhouse_get_client(
            host=host or "localhost",
            port=port,
            username=username,
            password=password,
            database=database,
            client_name="celeryviz"
        )

    def execute(self, query: str):
        return self.client.command(query)

    async def insert(self, table: str, data: List[List[Any]]):
        await asyncio.to_thread(self.client.insert, table, data,
                                column_names=_ClickhouseHelpers.column_order)
        
    async def query(self, query: str) -> Sequence[Sequence[Any]]:
        query_result = await asyncio.to_thread(self.client.query, query)
        return query_result.result_rows
    

class _ChdbClient(_AbstractClickhouseClient):
    def __init__(self, path=None):
        if not chdb:
            raise ImportError("chdb library is not installed.")

        self.connection = chdb.dbapi.connect(path=path) 
    
    async def insert(self, table: str, data: List[List[Any]]):
        cursor = self.connection.cursor()

        columns_count = len(_ClickhouseHelpers.column_order)
        columns_question_marks = ', '.join(['?'] * columns_count)

        insert_query = f'insert into {table} VALUES ({columns_question_marks})'
        await asyncio.to_thread(cursor.executemany, insert_query, data)

    async def query(self, query: str) -> Sequence[Sequence[Any]]:
        cursor = self.connection.cursor()
        await asyncio.to_thread(cursor.execute, query)
        return cursor.fetchall()

    def execute(self, query: str):
        cursor = self.connection.cursor()
        cursor.execute(query)


def _get_client(clickhouse_config: ClickhouseConfig):
    if clickhouse_config.engine == "MergeTree":
        return _HostedClickhouseClient(
            **clickhouse_config.get_connection_config()
        )
    else:
        return _ChdbClient(**clickhouse_config.get_connection_config())


class _ClickhouseHelpers:
    indexed_fields = {
        "timestamp",
        "uuid",
        "type",
        "hostname",
    }
    column_order = ('event_time', 'task_id', 'event_type', 'hostname',
                    'payload')

    @staticmethod
    def create_tables(client: _AbstractClickhouseClient, engine: str):
        """Create necessary Clickhouse tables if they do not exist."""
        database = "default"
        table = "task_events"
        engine_config = 'ENGINE = MergeTree' if engine == 'MergeTree' else ''

        ddl = f"""
        CREATE TABLE IF NOT EXISTS {database}.{table}
        (
            event_time DateTime64(3),
            task_id UUID,
            event_type LowCardinality(String),
            hostname LowCardinality(String),
            payload JSON
        )
        {engine_config}
        PARTITION BY toYYYYMM(event_time)
        ORDER BY (event_time, event_type, hostname, task_id)
        """

        # Execute the DDL statement against Clickhouse
        client.execute(ddl)

    @classmethod
    def convert_json_to_clickhouse_format(cls, json_data: List[dict]) -> List[List[Any]]:
        """Convert JSON data to a format suitable for Clickhouse insertion."""

        _empty_data = []
        rows: List[List[Any]] = [_empty_data] * len(json_data)

        for i, event in enumerate(json_data):
            ts = event["timestamp"]
            task_uuid = event["uuid"]
            event_type = event["type"]
            hostname = event["hostname"]

            # Build payload without indexed fields
            payload = {
                k: v for k, v in event.items()
                if k not in cls.indexed_fields
            }

            row = [
                datetime.fromtimestamp(ts),
                UUID(task_uuid),
                event_type,
                hostname,
                payload,
            ]

            rows[i] = row

        return rows
    
    @classmethod
    def convert_clickhouse_to_json_format(cls, rows: Sequence[Sequence[Any]]) -> List[dict]:
        """Convert Clickhouse rows back to JSON format."""
        json_data = []

        for row in rows:
            event_time, task_id, event_type, hostname, payload = row
            event = {
                "timestamp": event_time.timestamp(),
                "uuid": str(task_id),
                "type": event_type,
                "hostname": hostname,
            }
            event.update(payload)  # Merge payload into the event
            json_data.append(event)

        return json_data