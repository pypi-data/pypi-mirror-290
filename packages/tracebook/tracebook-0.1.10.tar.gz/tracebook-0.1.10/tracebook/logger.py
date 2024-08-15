# decorators.py
from functools import wraps

from tracebook.config import Config, LogLevel
from tracebook.logger_core import LoggerCore
from tracebook.utils import get_cpu_usage, get_memory_usage


class Logger:
    """
    Logger class for logging function calls, parameters, return values, and execution times.

    Parameters
    ----------
    config : Config
        The configuration object containing the logger settings.

    Methods
    -------
    trace : decorator
        A decorator function to log function calls, parameters, return values, and execution times.
    trace_inputs : decorator
        A decorator function that logs the inputs of a function.
    trace_outputs : decorator
        A decorator function to log function outputs.
    trace_exceptions : decorator
        A decorator function to catch and log exceptions raised by the decorated function.
    trace_resources : decorator
        Decorator function that logs the execution time, CPU usage, and memory usage of a function.
    debug : logging function
        Logs debug-level messages.
    info : logging function
        Logs information-level messages.
    warning : logging function
        Logs a warning-level message.
    error : logging function
        Logs error-level messages.
    critical : logging function
        Logs critical-level messages.
    """

    def __init__(self, config: Config):
        """
        Initialize the logger
        """
        self.logger = LoggerCore(config)

    def trace(
        self,
        log_inputs: bool = True,
        log_outputs: bool = True,
        log_exceptions: bool = True,
        log_resources: bool = False,
        blocking: bool = False,
    ):
        """
        A decorator function to log function calls, parameters, return values, and execution times.

        Parameters
        ----------
        log_inputs : bool
            Whether to log function inputs (default: True)
        log_outputs : bool
            Whether to log function outputs (default: True)
        log_exceptions : bool
            Whether to log exceptions (default: True)
        log_resources : bool
            Whether to log system resources (default: False)
        blocking : bool
            Whether to block the execution of the function if an exception occurs (default: False)

        Returns
        -------
        decorator
            A decorator function that logs the specified information
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if log_inputs:
                    self.logger.log_function_call(func.__name__, *args, **kwargs)
                try:
                    result = func(*args, **kwargs)
                    if log_outputs:
                        self.logger.log_function_exit(func.__name__, str(result))
                    return result
                except Exception as e:
                    if log_exceptions:
                        self.logger.log_exception(func.__name__, e)
                    if blocking:
                        raise e
                    else:
                        if log_outputs:
                            self.logger.log_function_exit(func.__name__, str(None))
                        return None
                finally:
                    if log_resources:
                        cpu_usage = get_cpu_usage()
                        memory_usage = get_memory_usage()
                        self.logger.log_details(f"{cpu_usage} {memory_usage}")

            return wrapper

        return decorator

    def trace_inputs(self):
        """
        A decorator function that logs the inputs of a function.

        Returns
        -------
        decorator
            A decorator function that logs the inputs of the decorated function.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.logger.log_function_call(func.__name__, *args, **kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def trace_outputs(self):
        """
        A decorator function to log function outputs.

        Returns
        -------
        decorator
            A decorator function that logs function outputs
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.logger.log_function_exit(func.__name__, str(result))
                return result

            return wrapper

        return decorator

    def trace_exceptions(self):
        """
        A decorator function to catch and log exceptions raised by the decorated function.

        Returns
        -------
        decorator
            A decorator function that catches and logs exceptions raised by the decorated function.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.logger.log_exception(func.__name__, e)
                    raise

            return wrapper

        return decorator

    def trace_resources(self):
        """
        Decorator function that logs the execution time, CPU usage, and memory usage of a function.

        Returns
        -------
        decorator
            The decorated function.

        Example
        -------
            @trace_resources
            def my_function(param1, param2):
                # function logic here

            my_function(1, 2)
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                import time

                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                cpu_usage = get_cpu_usage()
                memory_usage = get_memory_usage()
                self.logger.log_details(
                    f"Execution Time: {end_time - start_time} seconds, CPU Usage: {cpu_usage}, Memory Usage: {memory_usage}"
                )
                return result

            return wrapper

        return decorator

    def debug(self, *args):
        """
        Logs debug-level messages.

        Parameters
        ----------
        *args: Variable number of arguments to be logged.

        Returns
        -------
        None
        """
        self.logger.log_details(" ".join(args), LogLevel.DEBUG)

    def info(self, *args):
        """
        Logs information-level messages.

        Parameters
        ----------
        *args: Variable number of arguments to be logged.

        Returns
        -------
        None
        """
        self.logger.log_details(" ".join(args), LogLevel.INFO)

    def warning(self, *args):
        """
        Logs a warning-level message.

        Parameters
        ----------
        *args: Variable number of arguments to be logged.

        Returns
        -------
        None
        """
        self.logger.log_details(" ".join(args), LogLevel.WARNING)

    def error(self, *args):
        """
        Logs error-level messages.

        Parameters
        ----------
        *args: Variable number of arguments to be logged.

        Returns
        -------
        None
        """
        self.logger.log_details(" ".join(args), LogLevel.ERROR)

    def critical(self, *args):
        """
        Logs critical-level messages.

        Parameters
        ----------
        *args: Variable number of arguments to be logged.

        Returns
        -------
        None
        """
        self.logger.log_details(" ".join(args), LogLevel.CRITICAL)
