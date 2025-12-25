import asyncio
import logging
import socketio
from typing import List
from celeryviz.constants import CELERY_DATA_EVENT, CLIENT_NAMESPACE
from celeryviz.data_service.base import AbstractEventSink


logger = logging.getLogger(__name__)

    
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