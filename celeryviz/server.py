from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from uvicorn import Config, Server as UvicornServer
import logging
from fastapi import FastAPI
import socketio
from celeryviz.recorder import Recorder
from celeryviz.constants import (
    DEFAULT_PORT, SERVER_NAMESPACE, CLIENT_NAMESPACE, CELERY_DATA_EVENT, DEFAULT_LOG_FILE
)

banner_template = f"""
==================================
        🎉 App Launched!
==================================
🌐 URL: http://localhost:%d/app/
==================================
"""

logger = logging.getLogger(__name__)


class ClientNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        logger.info(f"Client connected: {sid}")

    def on_disconnect(self, sid):
        logger.info(f"Client disconnected: {sid}")

    async def on_message(self, sid, data):
        logger.debug(f'message received with {data}')
        await self.emit('reply', data=data, namespace=SERVER_NAMESPACE)


class Server:
    def __init__(self, loop: asyncio.AbstractEventLoop, record: bool = False, file: str = DEFAULT_LOG_FILE, port: int = DEFAULT_PORT):
        self.sio = socketio.AsyncServer(cors_allowed_origins='*', namespaces=[SERVER_NAMESPACE, CLIENT_NAMESPACE],
                                    async_mode='asgi')
        self.socket_app = socketio.ASGIApp(self.sio)
        self.app = FastAPI()
        self.record = record
        self.loop = loop
        self.file = file
        self.port = port

        if self.record:
            self.recorder = Recorder(file_name=file)
            logger.info("Recorder enabled")

        self.app.mount("/socket.io", self.socket_app)
        self.app.get("/app/", response_class=HTMLResponse)(self.frontend_app)
        self.app.mount("/", StaticFiles(directory="celeryviz/static"), name="static")
        self.sio.register_namespace(ClientNamespace('/client'))

    def frontend_app(self):
        return HTMLResponse(content=open("celeryviz/static/index.html").read(), status_code=200)

    async def event_handler(self, data):

        if self.record:
            self.recorder.record(data)

        await self.sio.emit(CELERY_DATA_EVENT, data=data, namespace=CLIENT_NAMESPACE)

    def start(self):
        banner = banner_template % self.port
        logger.info(banner)
        config = Config(app=self.app, host='0.0.0.0', port=self.port)
        server = UvicornServer(config=config)
        self.loop.run_until_complete(server.serve())
