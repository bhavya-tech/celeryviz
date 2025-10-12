import threading
import time
import unittest
import sys
from unittest.mock import AsyncMock, Mock, patch
from celery import Celery

from celeryviz.event_receiver import EventListener


class EventHandlerProcess(threading.Thread):
    """
    A separate process for `EventListener` thread to run in.
    Its not possile to kill a thread.
    """
    def __init__(self, app, event_handler, *args, **kwargs):
        self.event_listener = EventListener(app, event_handler, Mock())
        self.event_listener.daemon = True

        super().__init__(*args, **kwargs)

    def run(self):
        self.event_listener.start()

class TestEventListener(unittest.TestCase):

    def setUp(self) -> None:
        self.app = Celery('example_app', broker='redis://127.0.0.1:6379/0')
        self.event_handler_process = EventHandlerProcess(
            self.app, AsyncMock(), daemon=True)
        return super().setUp()

    def test_event_listener(self):
        """
        This tests the event handler is added to event loop and is called when celery event is emitted
        """

        with patch('celeryviz.event_receiver.EventListener.onEvent') \
            as mock_event_handler:

            self.event_handler_process.start()

            time.sleep(0.5)
            with self.app.events.default_dispatcher() as dispatcher:
                dispatcher.send('task-received', uuid='1234')

            time.sleep(0.5)
            mock_event_handler.assert_called_once()