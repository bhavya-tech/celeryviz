import multiprocessing
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
from celery import Celery

from socketio import Client

from celeryviz.constants import *
from celeryviz.executor import starter


class ClientThread(threading.Thread):
    def __init__(self, on_event):
        super().__init__()
        self.daemon = True
        self.client = Client(logger=False, engineio_logger=False)
        self.client.on(CELERY_DATA_EVENT, handler=on_event,
                  namespace=CLIENT_NAMESPACE)

    def run(self):
        self.client.connect('http://localhost:%s/' %
                       DEFAULT_PORT, wait=True, wait_timeout=5)
        self.client.wait()


class MockCtx:
    """
    Custom mock context class as unittest.mock.Mock does not pickle.
    """

    def __init__(self, app):
        self.obj = SimpleNamespace()
        self.obj.app = app


class TestIntegration(unittest.TestCase):
    """
    This test the backend end to end. It starts the server and client and checks if the client receives the event.
    """

    payload = {"utcoffset": -6, "uuid": "4897c640-a023-4cb8-ae8e-1df4641a3ba1", "name": "basic_task.add", "args": "()", "kwargs": "{}",
               "root_id": "4897c640-a023-4cb8-ae8e-1df4641a3ba1", "parent_id": None, "retries": 0, "eta": None, "expires": None, "timestamp": 1685367125.9317474, "type": "task-received"}

    def setUp(self) -> None:
        self.app = Celery('example_app', broker='redis://127.0.0.1:6379/0')
        self.mock_ctx = MockCtx(self.app)

        self.on_event = Mock()
        self.server_process = multiprocessing.Process(
            target=starter, args=[self.mock_ctx, False, "", DEFAULT_PORT], daemon=True)
        self.client_thread = ClientThread(self.on_event)
        return super().setUp()

    def test_integration(self):

        self.server_process.start()

        time.sleep(1)
        self.client_thread.start()
        time.sleep(1)

        with self.app.events.default_dispatcher() as dispatcher:
            dispatcher.send(**self.payload)
        
        time.sleep(1)
        self.assertIsSubDict(self.payload, self.on_event.call_args.args[0])

    def assertIsSubDict(self, subset, superset):
        for key, val in subset.items():
            self.assertEqual(val, superset[key])

    def tearDown(self) -> None:
        self.client_thread.client.disconnect()
        self.server_process.terminate()
        return super().tearDown()
