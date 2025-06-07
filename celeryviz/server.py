import logging
import os

import socketio
from aiohttp import web

from .constants import *
from .recorder import Recorder

library_path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)

banner = """
==================================
        🎉 App Launched!
==================================
🌐 URL: http://localhost:%d/app/
==================================
""" % SOCKETIO_HOST_PORT


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

    def __init__(self, loop, record: bool = False, file: str = DEFAULT_LOG_FILE):
        self.record = record
        self.file = file
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
        logger.info("\n" + banner)
        web.run_app(self.app, port=SOCKETIO_HOST_PORT, loop=self.loop,
                    print=None)

    async def event_handler(self, data):

        if self.record:
            self.recorder.record(data)

        await self.sio.emit(CELERY_DATA_EVENT, data=data, namespace=CLIENT_NAMESPACE)
