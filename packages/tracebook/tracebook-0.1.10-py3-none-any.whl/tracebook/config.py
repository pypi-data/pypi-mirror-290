# src/bookkeeping/config.py

from enum import Enum
from typing import Literal


class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class WebUIConfig:
    """
    Configuration for the web UI.
    """

    def __init__(
        self,
        title: str = "TraceBook",
        foreground_color: str = "#0056b3",
        background_color: str = "#E6F2FF",
        show_star_on_github: bool = True,
        indent_logs: bool = True,
        is_active: bool = True,
        port: int = 2234,
        refresh_interval: int = 1000,
        max_data_points: int = 100,
    ):
        """
        Initialize the web UI configuration.

        Args:
            title (str): The title of the web UI.
            foreground_color (str): The foreground color of the web UI.
            background_color (str): The background color of the web UI.
            show_star_on_github (bool): Whether to show the star on GitHub.
            indent_logs (bool): Whether to indent the logs.
            is_active (bool): Whether the web UI is active.
            port (int): The port to use for the web UI.
            refresh_interval (int): The refresh interval in milliseconds.
            max_data_points (int): The maximum number of data points to show.
        """
        self.title = title
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.show_star_on_github = show_star_on_github
        self.indent_logs = indent_logs
        self.is_active = is_active
        self.port = port
        self.refresh_interval = refresh_interval
        self.max_data_points = max_data_points



class RemoteConfig:
    """
    Configuration for remote logging.
    """

    def __init__(self, url, headers, use=True):
        """
        Initialize the remote configuration.

        Args:
            url (str): The URL of the remote logging server.
            headers (dict): The headers for the remote logging server.
            use (bool): Whether to use the remote logging server.
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
        output=Literal["console", "file", "both"],
        file_path=None,
        remote_config: RemoteConfig = None,
        web_config: WebUIConfig = None,
    ):
        """
        Initialize the configuration.

        Args:
            log_level (LogLevel): The log level to use.
            output (str): The output destination to use.
            file_path (str): The file path to use for logging.
            remote_config (RemoteConfig): The remote logging configuration.
            web_config (WebUIConfig): The web UI configuration.
        """
        self.log_level = log_level
        self.output = output
        self.file_path = file_path
        self.remote_config = remote_config or RemoteConfig(None, None, False)
        self.web_config = web_config or WebUIConfig()

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
