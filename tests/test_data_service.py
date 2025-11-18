import threading
import unittest
import tempfile
from fastapi import FastAPI
import socketio
import asyncio

from uvicorn import Config, Server as UvicornServer

from celeryviz.data_service import FileEventSink, SocketioEventSink
from celeryviz.constants import CELERY_DATA_EVENT, CLIENT_NAMESPACE
from tests.utils import get_free_ephemeral_port

class TestFileEventSink(unittest.IsolatedAsyncioTestCase):
    
    async def test_file_event_sink(self):
        test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl')
        sink = FileEventSink(test_file.name)

        test_events = [
            {"type": "task-received", "uuid": "1234"},
            {"type": "task-started", "uuid": "1234"}
        ]

        await sink.dump_events(test_events)

        with open(test_file.name, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[0].strip(), '{"type": "task-received", "uuid": "1234"}')
            self.assertEqual(lines[1].strip(), '{"type": "task-started", "uuid": "1234"}')


class TestSocketioEventSink(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.port = get_free_ephemeral_port()
        return super().setUp()

    def _run_fastapi_server(self, socket_app):
        fastapi_app = FastAPI()
        fastapi_app.mount("/socket.io", socket_app)
        config = Config(app=fastapi_app, host='0.0.0.0', port=self.port)
        server = UvicornServer(config=config)
        asyncio.run(server.serve())

    async def test_socketio_event_sink(self):
        sink = SocketioEventSink()

        server_thread = threading.Thread(target=self._run_fastapi_server, args=(sink.socket_app,), daemon=True)
        server_thread.start()

        test_events = [
            {"type": "task-received", "uuid": "5678"},
            {"type": "task-started", "uuid": "5678"}
        ]

        received_events = []
        async def on_event(data):
            received_events.append(data)

        client = socketio.AsyncClient()
        client.on(CELERY_DATA_EVENT, on_event, namespace=CLIENT_NAMESPACE)

        await asyncio.sleep(1)  # Wait for server to start
        await client.connect('http://0.0.0.0:%d' % self.port)

        for event in test_events:
            await sink.dump_events([event])

        await asyncio.sleep(1)  # Wait to ensure all events are received
        await client.disconnect()

        self.assertEqual(len(received_events), 2)
        self.assertEqual(received_events[0], test_events[0])
        self.assertEqual(received_events[1], test_events[1])
