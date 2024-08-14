# src/bookkeeping/__init__.py

from .config import Config, LogLevel
# from .decorators import log_function
from .logger import Logger
# from .remote_handler import log_push_file_to_remote_server
# from .utils import current_timestamp, format_stack_trace

__all__ = [
    "Logger",
    "LogLevel",
    "Config",
    # "log_function",
    # "current_timestamp",
    # "format_stack_trace",
    # "log_push_file_to_remote_server",
]




logger = Logger(
    config=Config(log_level=LogLevel.INFO, output="both", file_path="test.log")
)


@logger.trace()
def num(i, j):
    return j + j



if __name__ == "__main__":
    print(num(1, 2))