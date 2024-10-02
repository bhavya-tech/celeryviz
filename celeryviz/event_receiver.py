import asyncio
import logging
import threading

from celery.events.receiver import EventReceiver

from .constants import *

logger = logging.getLogger(__name__)


class EventListener(threading.Thread):
    def onEvent(self, event):
        logger.debug("Event received")
        asyncio.run_coroutine_threadsafe(
            self.event_handler(event), self.server_loop)

    def __init__(self, app, event_handler, server_loop):
        super().__init__(daemon=True)
        self.app = app
        self.event_handler = event_handler
        self.server_loop = server_loop

    def run(self):
        handler = {
            'task-failed': self.onEvent,
            'task-received': self.onEvent,
            'task-revoked': self.onEvent,
            'task-started': self.onEvent,
            'task-succeeded': self.onEvent,
            'task-retried': self.onEvent,
            'task-rejected': self.onEvent,
            'task-log': self.onEvent,
        }
        while True:
            try:
                with self.app.connection() as conn:
                    recv = EventReceiver(conn, handlers=handler, app=self.app)

                    recv.capture(limit=None, timeout=None, wakeup=True)

            except (KeyboardInterrupt, SystemExit):
                try:
                    import _thread as thread
                except ImportError:
                    import thread

                thread.interrupt_main()

            except Exception as exc:
                logger.info('Connection error: %r' % (exc, ))
