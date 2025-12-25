import asyncio
import logging
import aiofiles
import json
import socketio
from typing import List

from celeryviz.constants import CELERY_DATA_EVENT, CLIENT_NAMESPACE

logger = logging.getLogger(__name__)


class AbstractEventSink:
    """Abstract service for dumping event data."""

    async def dump_events(self, events: List[dict]):
        """Dump a list of event dictionaries to the data store."""
        raise NotImplementedError("Subclasses must implement dump_events method.")


class AbstractEventRetriever:
    """
    Abstract service for querying event data.
    Not in use currently, will be used when we start sending stored events to clients.
    """

    async def fetch_events(self, *args, **kwargs) -> List[dict]:
        """Receive a list of event dictionaries from the data source."""
        raise NotImplementedError("Subclasses must implement fetch_events method.")


class FileEventSink(AbstractEventSink):
    """File-based implementation of the AbstractEventSink."""

    def __init__(self, file_path: str):

        if file_path.endswith('.jsonl') or file_path.endswith('.ndjson'):
            self.file_path = file_path
            logger.info(f"Initialized event storage with file: {file_path}")
        else:
            raise ValueError("File extension must be .jsonl or .ndjson")

    async def dump_events(self, events: List[dict]):
        """Dump a list of event dictionaries to a file."""

        json_lines = [json.dumps(event) for event in events]
        write_data = "\n".join(json_lines) + "\n"

        async with aiofiles.open(self.file_path, "a") as f:
            await f.write(write_data)


class SocketioEventSink(AbstractEventSink):
    """Socket.IO implementation of the AbstractEventSink."""

    class ClientNamespace(socketio.AsyncNamespace):
        def on_connect(self, sid, environ):
            logger.info(f"Client connected: {sid}")

        def on_disconnect(self, sid):
            logger.info(f"Client disconnected: {sid}")

    def __init__(self):
        self.sio = socketio.AsyncServer(cors_allowed_origins='*', namespaces=[CLIENT_NAMESPACE],
                                    async_mode='asgi')
        self.socket_app = socketio.ASGIApp(self.sio)
        self.sio.register_namespace(self.ClientNamespace(CLIENT_NAMESPACE))

        logger.info("Initialized Socket.IO event broadcasting.")

    async def _emit_event(self, event: dict):
        await self.sio.emit(CELERY_DATA_EVENT, data=event, namespace=CLIENT_NAMESPACE)

    async def dump_events(self, events: List[dict]):
        """Emit each event dictionary to the Socket.IO client."""

        event_futures = [self._emit_event(event) for event in events]
        await asyncio.gather(*event_futures)