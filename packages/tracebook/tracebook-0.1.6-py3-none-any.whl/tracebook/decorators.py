# decorators.py
from functools import wraps

from tracebook.config import Config
from tracebook.logger_core import LoggerCore
from tracebook.utils import get_cpu_usage, get_memory_usage


class Logger:
    def __init__(self, config: Config):
        self.logger = LoggerCore(config)

    def trace(
        self,
        log_inputs: bool = True,
        log_outputs: bool = True,
        log_exceptions: bool = True,
        log_resources: bool = False,
        blocking:bool=False,
    ):
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
                        return None
                finally:
                    if log_resources:
                        cpu_usage = get_cpu_usage()
                        memory_usage = get_memory_usage()
                        self.logger.log_details(f"{cpu_usage} {memory_usage}")

            return wrapper

        return decorator

    def trace_inputs(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.logger.log_function_call(func.__name__, *args, **kwargs)
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def trace_outputs(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.logger.log_function_exit(func.__name__, str(result))
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
                    self.logger.log_exception(func.__name__, e)
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
                self.logger.log_details(
                    f"Execution Time: {end_time - start_time} seconds, CPU Usage: {cpu_usage}, Memory Usage: {memory_usage}"
                )
                return result

            return wrapper

        return decorator
