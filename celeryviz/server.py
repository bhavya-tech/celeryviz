from typing import List
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from uvicorn import Config, Server as UvicornServer
import logging
from fastapi import FastAPI
from celeryviz.data_service import AbstractEventSink, SocketioEventSink, AbstractEventRetriever
from celeryviz.constants import DEFAULT_PORT

banner_template = f"""
==================================
        🎉 App Launched!
==================================
🌐 URL: http://localhost:%d/app/
==================================
"""

logger = logging.getLogger(__name__)

class Server:
    def __init__(self,
                 loop: asyncio.AbstractEventLoop,
                 port: int = DEFAULT_PORT,
                 event_data_sinks: List[AbstractEventSink] | None = None,
                 event_data_retrievers: List[AbstractEventRetriever] | None = None):
        self.app = FastAPI()
        self.loop = loop
        self.port = port
        self.event_data_sinks = event_data_sinks or []
        self.event_data_retrievers = event_data_retrievers or []
        self._mount_socketio_app()
        self._mount_event_retriever_endpoints()
        self.app.get("/app/", response_class=HTMLResponse)(self.frontend_app)
        self.app.mount("/", StaticFiles(directory="celeryviz/static"), name="static")

    def _mount_socketio_app(self):
        socketio_sink = next((sink for sink in self.event_data_sinks
                                if isinstance(sink, SocketioEventSink)), None)
        if socketio_sink:
            self.app.mount("/socket.io", socketio_sink.socket_app)

    def _mount_event_retriever_endpoints(self):
        for retriever in self.event_data_retrievers:
            endpoint = f"/data/{retriever.url_endpoint_name}/"
            self.app.get(endpoint)(retriever.fetch_events)

    def frontend_app(self):
        return HTMLResponse(content=open("celeryviz/static/index.html").read(), status_code=200)

    async def event_handler(self, data):
        """
        The `dump_events` if called for each event received for now.
        This can be optimized to batch process events in future.
        """

        sink_datadump_futures = [sink.dump_events([data])
                                 for sink in self.event_data_sinks]
        await asyncio.gather(*sink_datadump_futures)

    def start(self):
        banner = banner_template % self.port
        logger.info(banner)
        config = Config(app=self.app, host='0.0.0.0', port=self.port)
        server = UvicornServer(config=config)
        self.loop.run_until_complete(server.serve())
