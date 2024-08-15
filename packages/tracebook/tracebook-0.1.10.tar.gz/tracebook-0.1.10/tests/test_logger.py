import unittest
from unittest.mock import mock_open, patch, ANY

from tracebook.config import Config, LogLevel, RemoteConfig
from tracebook.logger_core import LoggerCore


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            output="both",
            log_level=LogLevel.DEBUG,  # noqa: F821
            file_path="test.log",
            remote_config=RemoteConfig(None, None, True),
        )
        self.logger = LoggerCore(self.config)

    @patch("tracebook.logger.log_push_file_to_remote_server")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_message_console_and_file(self, mock_open, mock_remote):
        self.logger._save_message("Test message")
        mock_open.assert_called_once_with("test.log", "a")
        handle = mock_open()
        handle.write.assert_called_once_with("[INFO] Test message\n")
        mock_remote.assert_called_once_with(self.config)

    @patch("tracebook.logger.logging.info")
    def test_log_function_enter(self, mock_info):
        with patch("tracebook.logger.current_timestamp", return_value="timestamp"):
            self.logger.log_function_enter("test_func", "param1, param2")
            message = "[INFO] timestamp > test_func param1, param2"
            mock_info.assert_called_once_with(message)

    @patch("tracebook.logger.logging.info")
    def test_log_function_exit(self, mock_info):
        with patch("tracebook.logger.current_timestamp", return_value="timestamp"):
            self.logger.log_function_exit("test_func", "result1")
            message = "[INFO] timestamp < test_func result1"
            mock_info.assert_called_once_with(message)

    @patch("tracebook.logger.logging.info")
    def test_log_function_call(self, mock_info):
        with patch("tracebook.logger.current_timestamp", return_value="timestamp"):
            self.logger.log_function_call("test_func", "arg1", kwarg1="value1")
            message = "[INFO] timestamp > test_func ('arg1',) {'kwarg1': 'value1'}"
            mock_info.assert_called_once_with(message)

    @patch("tracebook.logger.logging.error")
    def test_log_exception(self, mock_error):
        with patch("tracebook.logger.current_timestamp", return_value="timestamp"):
            self.logger.log_exception("test_func", Exception("Test exception"))
            message = "[ERROR] timestamp | test_func Test exception"
            mock_error.assert_called_once_with(message)

    @patch("tracebook.logger.current_timestamp", return_value="timestamp")
    def test_generate_message(self, mock_timestamp):
        result = self.logger._generate_message(">", "Test message")
        self.assertEqual(result, "timestamp > Test message")


class TestLoggerDecorators(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            output="both",
            log_level=LogLevel.DEBUG,
            file_path="test.log",
            remote_config=RemoteConfig(None, None, True),
        )
        self.logger = LoggerCore(self.config)

    @patch("tracebook.logger.Logger.log_function_call")
    @patch("tracebook.logger.Logger.log_function_exit")
    def test_trace_decorator(self, mock_log_exit, mock_log_call):
        @self.logger.trace()
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)
        mock_log_call.assert_called_once_with("test_func", 2, 3)
        mock_log_exit.assert_called_once_with("test_func", "5")
        self.assertEqual(result, 5)

    @patch("tracebook.logger.Logger.log_function_call")
    def test_trace_inputs_decorator(self, mock_log_call):
        @self.logger.trace_inputs()
        def test_func(x, y):
            return x + y

        test_func(2, 3)
        mock_log_call.assert_called_once_with("test_func", 2, 3)

    @patch("tracebook.logger.Logger.log_function_exit")
    def test_trace_outputs_decorator(self, mock_log_exit):
        @self.logger.trace_outputs()
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)
        mock_log_exit.assert_called_once_with("test_func", "5")
        self.assertEqual(result, 5)

    @patch("tracebook.logger.Logger.log_exception")
    def test_trace_exceptions_decorator(self, mock_log_exception):
        @self.logger.trace_exceptions()
        def test_func():
            raise ValueError("Test exception")

        with self.assertRaises(ValueError):
            test_func()
        mock_log_exception.assert_called_once_with("test_func", ANY)

    @patch("tracebook.logger.Logger.log_details")
    def test_trace_resources_decorator(self, mock_log_details):
        @self.logger.trace_resources()
        def test_func():
            return "result"

        with patch("tracebook.utils.get_cpu_usage", return_value="10%"):
            with patch("tracebook.utils.get_memory_usage", return_value="512MB"):
                test_func()
                # called functin times


if __name__ == "__main__":
    unittest.main()
