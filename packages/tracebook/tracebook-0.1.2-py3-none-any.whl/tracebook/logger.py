import logging
from functools import wraps
from typing import Literal
from tracebook.config import Config, LogLevel
from tracebook.dashboard import RealTimeDashboard
from tracebook.remote_handler import log_push_file_to_remote_server
from tracebook.utils import current_timestamp, get_memory_usage, get_cpu_usage


class Logger:
    def __init__(self, config: Config):
        self.config = config
        with open(self.config.file_path, "a") as file:
            file.write(f"=== Starting TraceBook at {current_timestamp()} ===\n")
        if self.config.remote_config.use:
            log_push_file_to_remote_server(self.config)

        if self.config.show_web:
            self.dashboard = RealTimeDashboard(
                self.config.file_path, self.config.web_port
            )
            self.dashboard.run()
        else:
            self.dashboard = None

    def _save_message(self, message: str, level: LogLevel = LogLevel.INFO):
        level_str = level.name
        full_message = f"[{level_str}] {message}"

        if self.config.output == "console" or self.config.output == "both":
            self._log_to_console(full_message, level)

        if self.config.output == "file" or self.config.output == "both":
            with open(self.config.file_path, "a") as file:
                file.write(full_message + "\n")
            if self.config.remote_config.use:
                log_push_file_to_remote_server(self.config)

    def _log_to_console(self, message: str, level: LogLevel):
        log_method = {
            LogLevel.DEBUG: logging.debug,
            LogLevel.INFO: logging.info,
            LogLevel.WARNING: logging.warning,
            LogLevel.ERROR: logging.error,
            LogLevel.CRITICAL: logging.critical,
        }.get(level, logging.info)
        log_method(message)

    def log_function_enter(self, function_name: str, parameters: str):
        message = self._generate_message(">", f"{function_name} {parameters}")
        self._save_message(message, LogLevel.INFO)

    def log_function_exit(self, function_name: str, result: str):
        message = self._generate_message("<", f"{function_name} {result}")
        self._save_message(message, LogLevel.INFO)

    def log_function_call(self, function_name: str, *args, **kwargs):
        parameters = f"{args} {kwargs}"
        self.log_function_enter(function_name, parameters)

    def log_exception(self, function_name: str, exception: Exception):
        message = self._generate_message("|", f"{function_name} {str(exception)}")
        self._save_message(message, LogLevel.ERROR)

    def log_details(self, message: str, level: LogLevel = LogLevel.INFO):
        message = self._generate_message("*", message)
        self._save_message(message, level)

    def _generate_message(self, operation_symbol: Literal[">", "<", "|", "*"], message):
        return f"{current_timestamp()} {operation_symbol} {message}"

    # Decorators as methods
    def trace(
        self,
        log_inputs: bool = True,
        log_outputs: bool = True,
        log_exceptions: bool = True,
        log_resources: bool = False,
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if log_inputs:
                    self.log_function_call(func.__name__, *args, **kwargs)
                try:
                    result = func(*args, **kwargs)
                    if log_outputs:
                        self.log_function_exit(func.__name__, str(result))
                    return result
                except Exception as e:
                    if log_exceptions:
                        self.log_exception(func.__name__, e)
                    raise
                finally:
                    if log_resources:
                        cpu_usage = get_cpu_usage()
                        memory_usage = get_memory_usage()
                        self.log_details(
                            f"{cpu_usage} {memory_usage}"
                        )

            return wrapper

        return decorator

    def trace_inputs(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.log_function_call(func.__name__, *args, **kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def trace_outputs(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.log_function_exit(func.__name__, str(result))
                return result

            return wrapper

        return decorator

    def trace_exceptions(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.log_exception(func.__name__, e)
                    raise

            return wrapper

        return decorator

    def trace_resources(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                import time

                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                cpu_usage = get_cpu_usage()
                memory_usage = get_memory_usage()
                self.log_details(
                    f"Execution Time: {end_time - start_time} seconds, CPU Usage: {cpu_usage}, Memory Usage: {memory_usage}"
                )
                return result

            return wrapper

        return decorator
