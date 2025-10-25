import unittest
from unittest.mock import Mock, patch

from celeryviz.constants import DEFAULT_PORT
from celeryviz.executor import starter


class TestStarter(unittest.TestCase):
    def test_starter(self):

        mock_ctx = Mock()
        mock_record = Mock()

        with patch('celeryviz.executor.EventListener') as mock_event_listener,\
                patch('celeryviz.executor.Server') as mock_server:

            starter(mock_ctx, mock_record, "", DEFAULT_PORT)

            # Check if events are being enabled
            mock_ctx.obj.app.control.enable_events.assert_called_once()

            # Check if server and event listener are being started
            mock_server.assert_called_once()
            mock_server.return_value.start.assert_called_once()
            mock_event_listener.assert_called_once()
            mock_event_listener.return_value.start.assert_called_once()
