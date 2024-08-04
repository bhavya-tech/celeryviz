import unittest
from unittest.mock import Mock, patch

from celeryviz.server import Server
from utils import ServerTestCase


class TestServerFeatures(unittest.TestCase):
    def test_recorder(self):
        mock_filename = str(self) + 'mock_filename'

        with patch('celeryviz.server.Recorder') as mock_recorder:
            Server(Mock(), record=True, file=mock_filename)
            mock_recorder.assert_called_once_with(file_name=mock_filename)


class TestServerRunning(ServerTestCase):
    def test_server_running(self):
        async def test(client):
            resp = await client.get('/app/')
            self.assertEqual(resp.status, 200)

        self.client_test(test)
