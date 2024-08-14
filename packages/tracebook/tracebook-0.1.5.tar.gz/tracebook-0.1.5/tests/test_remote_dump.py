import unittest
from unittest.mock import patch, mock_open
from tracebook.config import Config, LogLevel, RemoteConfig
from tracebook.remote_handler import log_push_file_to_remote_server

class TestRemoteDump(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(
            output="both",
            log_level=LogLevel.DEBUG,
            file_path="test.log",
            remote_config=RemoteConfig(url="http://example.com/upload", headers={}),
        )

    @patch("tracebook.remote_handler.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="log data")
    def test_log_push_file_to_remote_server_success(self, mock_open, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.text = "Success"

        log_push_file_to_remote_server(self.config)

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], self.config.remote_config.url)
        self.assertEqual(kwargs.get('headers'), self.config.remote_config.headers)
        self.assertIn('files', kwargs)
        files = kwargs['files']

        file_mock = files['file']
        file_mock.seek(0)  # Ensure we're at the beginning of the file
        self.assertEqual(file_mock.read(), "log data")

    @patch("tracebook.remote_handler.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="log data")
    def test_log_push_file_to_remote_server_failure(self, mock_open, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.text = "Error"

        log_push_file_to_remote_server(self.config)

        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], self.config.remote_config.url)
        self.assertEqual(kwargs.get('headers'), self.config.remote_config.headers)
        self.assertIn('files', kwargs)
        files = kwargs['files']
        file_mock = files['file']
        file_mock.seek(0)  # Ensure we're at the beginning of the file
        self.assertEqual(file_mock.read(), "log data")

if __name__ == "__main__":
    unittest.main()
