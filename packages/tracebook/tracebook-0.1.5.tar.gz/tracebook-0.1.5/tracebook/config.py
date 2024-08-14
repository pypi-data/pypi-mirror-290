# src/bookkeeping/config.py

from enum import Enum
from typing import Literal


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class RemoteConfig:
    """
    Configuration for remote logging.
    """

    def __init__(self, url, headers, use=True):
        """
        Initialize the remote configuration.

        Args:
            url (str): The URL of the remote logging server.
            token (str): The authentication token for the remote logging server.
        """
        self.url = url
        self.headers = headers
        self.use = use


class Config:
    """
    Configuration class for the Trace Book logging system.
    """

    def __init__(
        self,
        log_level=LogLevel.INFO,
        show_web = True,
        web_port=2234,
        output=Literal["console", "file", "both"],
        file_path=None,
        remote_config: RemoteConfig = None,
    ):
        """
        Initialize the configuration.

        Args:
            log_level (LogLevel): The minimum level of logs to capture.
            output (str): Where to send the logs ('console', 'file', or 'both').
            file_path (str): The path to the log file (required if output includes 'file').
            remote_config (dict): Configuration for remote logging (optional).
        """
        self.log_level = log_level
        self.output = output
        self.show_web = show_web
        self.web_port = web_port
        self.file_path = file_path
        self.remote_config = remote_config or RemoteConfig(None, None, False)

    def get_log_level(self):
        """
        Get the configured log level.

        Returns:
            LogLevel: The configured log level.
        """
        return self.log_level

    def get_output(self):
        """
        Get the configured output destination.

        Returns:
            str: The configured output destination.
        """
        return self.output

    def get_file_path(self):
        """
        Get the configured file path for logging.

        Returns:
            str: The configured file path, or None if not configured.
        """
        return self.file_path

    def get_remote_config(self):
        """
        Get the remote logging configuration.

        Returns:
            dict: The remote logging configuration.
        """
        return self.remote_config
