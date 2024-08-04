from collections.abc import Coroutine
import unittest
from unittest.mock import Mock

from celeryviz.server import Server
from aiohttp.test_utils import AioHTTPTestCase, loop_context, TestClient, TestServer as AioHTTPTestServer


class ServerTestCase(unittest.TestCase):

    def client_test(self, test_func: Coroutine):
        server = Server(Mock())
        with loop_context() as loop:
            client = TestClient(AioHTTPTestServer(server.app, loop=loop))
            
            loop.run_until_complete(client.start_server())

            loop.run_until_complete(test_func(client))

            loop.run_until_complete(client.close())




