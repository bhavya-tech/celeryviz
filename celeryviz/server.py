import logging
import os

import socketio
from aiohttp import web

# Import the renamed DEFAULT_PORT constant
from .constants import DEFAULT_PORT, SERVER_NAMESPACE, CLIENT_NAMESPACE, CELERY_DATA_EVENT, DEFAULT_LOG_FILE
from .recorder import Recorder

library_path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)

# Banner will be formatted later in start() method
banner_template = """
==================================
        🎉 App Launched!
==================================
🌐 URL: http://localhost:%d/app/
==================================
"""


class ClientNapespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        logger.info("Client connected")

    def on_disconnect(self, sid):
        logger.info("Client disconnected")

    async def on_message(self, sid, data):
        logger.debug('message received with ', data)
        await self.emit('reply', data=data, namespace=SERVER_NAMESPACE)


class ServerNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        logger.info("Server connected")

    def on_disconnect(self, sid):
        logger.info("Server disconnected")

    async def on_message(self, sid, data):
        logger.debug('message received with ', data)
        await self.emit(CELERY_DATA_EVENT, data=data, namespace=CLIENT_NAMESPACE)


async def frontend_app(request):
    return web.FileResponse(f'{library_path}/static/index.html')


class Server:
    sio = socketio.AsyncServer(cors_allowed_origins='*', namespaces=[SERVER_NAMESPACE, CLIENT_NAMESPACE],
                               async_mode='aiohttp')

    # Add 'port' parameter to __init__
    def __init__(self, loop, record: bool = False, file: str = DEFAULT_LOG_FILE, port: int = DEFAULT_PORT):
        self.record = record
        self.file = file
        self.port = port # Store the port
        if self.record:
            self.recorder = Recorder(file_name=file)
            logger.info("Recorder enabled")

        self.sio.register_namespace(ServerNamespace(SERVER_NAMESPACE))
        self.sio.register_namespace(ClientNapespace(CLIENT_NAMESPACE))

        self.loop = loop

        self.app = web.Application()

        self.sio.attach(self.app)

        self.app.router.add_get('/app/', frontend_app)
        self.app.router.add_static(
            '/', path=f'{library_path}/static/', name='static')

    def start(self):
        # Format the banner here using self.port
        banner = banner_template % self.port
        logger.info("\n" + banner)
        # Use self.port here
        web.run_app(self.app, port=self.port, loop=self.loop,
                    print=None) # Keep print=None if that's the desired behavior

    async def event_handler(self, data):

        if self.record:
            self.recorder.record(data)

        await self.sio.emit(CELERY_DATA_EVENT, data=data, namespace=CLIENT_NAMESPACE)
