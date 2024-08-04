import unittest
from unittest.mock import mock_open, patch

from celeryviz.recorder import Recorder


class TestRecorder(unittest.TestCase):
    def test_recorder(self):
        mock_filename = 'test.txt'
        mock_dict_data = {'key': 'value'}

        with patch('builtins.open', mock_open(read_data='data')) as m:
            recorder = Recorder(file_name=mock_filename)
            recorder.record(mock_dict_data)

            m.assert_called_once_with(mock_filename, 'a')
