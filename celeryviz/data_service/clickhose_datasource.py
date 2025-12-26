import asyncio
from datetime import datetime, timezone
from uuid import UUID
from typing import Any, List
from celeryviz.data_service.base import AbstractEventSink, AbstractEventRetriever
from clickhouse_connect import get_client
import logging

logger = logging.getLogger(__name__)


class ClickhouseSink(AbstractEventSink):
    """Clickhouse implementation of the AbstractEventSink."""

    config_options = ('clickhouse_host', 'clickhouse_port', 'clickhouse_database',
                     'clickhouse_username', 'clickhouse_password', 'clickhouse_engine')

    def __init__(self, clickhouse_config: dict):
        logger.info("Initializing ClickhouseSink")

        self.client = _ClickhouseClient(
            host=clickhouse_config.get("clickhouse_host"),
            port=clickhouse_config.get("clickhouse_port", 8123),
            username=clickhouse_config.get("clickhouse_username"),
            password=clickhouse_config.get("clickhouse_password", ""),
            database=clickhouse_config.get("clickhouse_database", "default")
        )

        engine = clickhouse_config.get("clickhouse_engine", "MergeTree")
        _ClickhouseHelpers.create_tables(self.client, engine=engine)

    async def dump_events(self, events: List[dict]):
        """Insert a list of event dictionaries into Clickhouse."""
        rows = _ClickhouseHelpers.convert_json_to_clickhouse_format(events)
        await self.client.insert("task_events", rows)


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