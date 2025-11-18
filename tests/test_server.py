import asyncio
import unittest

from fastapi.testclient import TestClient

import celeryviz.server


class TestServerRunning(unittest.TestCase):
    def setUp(self) -> None:
        self.server = celeryviz.server.Server(loop=asyncio.new_event_loop())
        return super().setUp()

    def test_is_webapp_served(self):
        """
        Test if the web app is being served at the correct endpoint.
        """

        with TestClient(self.server.app, base_url='http://localhost:9095') as client:
            response = client.get('/app/')
            self.assertEqual(response.status_code, 200)
