import asyncio
from datetime import datetime
from uuid import UUID
from typing import Any, List, Sequence
from celeryviz.data_service.base import AbstractConfigurableService, AbstractEventSink, AbstractEventRetriever
from clickhouse_connect import get_client
import logging

logger = logging.getLogger(__name__)


class ClickhouseConfig(AbstractConfigurableService):

    config_options = ('clickhouse_host', 'clickhouse_port', 'clickhouse_database',
                     'clickhouse_username', 'clickhouse_password', 'clickhouse_engine')
    
    @staticmethod
    def is_enabled(config: dict) -> bool:
        return config.get("clickhouse_enable", False)
    
    def __init__(self, config: dict):
        self.config = config

    def get_connection_config(self) -> dict:
        return {
            "host": self.config.get("clickhouse_host"),
            "port": self.config.get("clickhouse_port", 8123),
            "username": self.config.get("clickhouse_username"),
            "password": self.config.get("clickhouse_password", ""),
            "database": self.config.get("clickhouse_database", "default")
        }
    
    def get_engine(self) -> str:
        return self.config.get("clickhouse_engine", "MergeTree")


class ClickhouseSink(AbstractEventSink):
    """Clickhouse implementation of the AbstractEventSink."""

    def __init__(self, clickhouse_config: ClickhouseConfig):
        logger.info("Initializing ClickhouseSink")

        self.client = _ClickhouseClient(
            **clickhouse_config.get_connection_config()
        )

        engine = clickhouse_config.get_engine()
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

        self.client = _ClickhouseClient(
            **clickhouse_config.get_connection_config()
        )

    async def fetch_events(self, start_time: datetime, end_time: datetime) -> List[dict]:
        """Retrieve events from Clickhouse within the specified time range."""

        query = """
        SELECT event_time, task_id, event_type, hostname, payload
        FROM task_events
        WHERE event_time >= {start_time: DateTime}
          AND event_time <= {end_time: DateTime}
        ORDER BY event_time ASC
        """

        result = await _ClickhouseClient.query(self.client, query, params={
            "start_time": start_time,
            "end_time": end_time
        })

        events = _ClickhouseHelpers.convert_clickhouse_to_json_format(result)
        return events


class _ClickhouseClient:
    def __init__(self, host=None, port=8123, username=None, password="", database="default"):
        self.client = get_client(
            host=host or "localhost",
            port=port,
            username=username,
            password=password,
            database=database,
            client_name="celeryviz"
        )

    def execute(self, query: str):
        return self.client.command(query)

    async def insert(self, table: str, data: List[List[dict]]):
        await asyncio.to_thread(self.client.insert, table, data,
                                column_names=_ClickhouseHelpers.column_order)
        
    async def query(self, query: str, params: dict) -> Sequence[Sequence[Any]]:
        query_result = await asyncio.to_thread(self.client.query, query, parameters=params)
        return query_result.result_rows


class _ClickhouseHelpers:
    indexed_fields = {
        "timestamp",
        "uuid",
        "type",
        "hostname",
    }
    column_order = ['event_time', 'task_id', 'event_type', 'hostname',
                    'payload']

    @staticmethod
    def create_tables(client: _ClickhouseClient, engine: str = "MergeTree"):
        """Create necessary Clickhouse tables if they do not exist."""
        database = "default"
        table = "task_events"

        ddl = """
        CREATE TABLE IF NOT EXISTS {db}.{table}
        (
            event_time DateTime64(3),
            task_id UUID,
            event_type LowCardinality(String),
            hostname LowCardinality(String),
            payload JSON
        )
        ENGINE = {engine}
        PARTITION BY toYYYYMM(event_time)
        ORDER BY (event_time, event_type, hostname, task_id)
        """

        formatted_ddl = ddl.format(db=database, table=table, engine=engine)

        # Execute the DDL statement against Clickhouse
        client.execute(formatted_ddl)

    @classmethod
    def convert_json_to_clickhouse_format(cls, json_data: List[dict]) -> List[List[Any]]:
        """Convert JSON data to a format suitable for Clickhouse insertion."""
        # Implement conversion logic if necessary
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