import asyncio
import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from celeryviz.server import Server
import celeryviz.server


class TestServerFeatures(unittest.TestCase):
    def test_recorder(self):
        mock_filename = str(self) + 'mock_filename'

        with patch('celeryviz.server.Recorder') as mock_recorder:
            Server(Mock(), record=True, file=mock_filename)
            mock_recorder.assert_called_once_with(file_name=mock_filename)


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
