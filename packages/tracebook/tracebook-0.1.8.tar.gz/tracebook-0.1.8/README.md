Here's the updated README with the new configuration details integrated:

# Trace Book

**Trace Book** is a Python package designed for comprehensive code bookkeeping. It provides tools to log function calls, parameters, return values, and execution times. Additionally, it supports decorators for easy integration, automatic error tracking, and remote log transmission, all with customizable log levels and output configurations.

![UI](./example/example-ui.png)

## Features

- **Function Logging**: Track function calls, parameters, return values, and execution times.
- **Automatic Error Tracking**: Log exceptions and stack traces automatically.
- **Decorators**: Simplify logging with decorators that track function parameters and results.
- **Remote Log Transmission**: Securely send logs to a remote server.
- **Customizable Log Levels**: Control log verbosity with DEBUG, INFO, WARNING, and ERROR levels.
- **Configurable Output**: Choose between logging to console, files, or transmitting logs to a remote server.
- **Web UI**: Visualize logs and system performance metrics through a customizable dashboard.

## Installation

You can install **Trace Book** using `pip`:

```bash
pip install tracebook
```

Or by cloning the repository and installing it manually:

```bash
git clone https://github.com/yourusername/tracebook.git
cd tracebook
pip install .
```

## Usage

### Basic Logging

```python
from tracebook import Logger
from tracebook.config import Config, LogLevel

logger = Logger(config=Config(log_level=LogLevel.INFO, output="both", file_path="app.log"))

@logger.trace()
def add(a, b):
    return a + b

result = add(3, 5)
print(f"Result: {result}")
```

### Logging with Resource Tracking

```python
@logger.trace(log_resources=True)
def compute_factorial(n):
    if n == 0:
        return 1
    return n * compute_factorial(n - 1)

compute_factorial(5)
```

### Using Different Log Levels

```python
logger.debug("Debugging information")
logger.info("General information")
logger.warning("Warning: resource running low")
logger.error("Error occurred: unable to connect")
logger.critical("Critical: system shutdown imminent")
```

### Exception Handling

```python
@logger.trace()
def divide(a, b):
    return a / b

try:
    divide(10, 0)
except ZeroDivisionError:
    logger.error("Attempted division by zero")
```

### Remote Logging Configuration

```python
from tracebook.config import RemoteConfig

remote_logger = Logger(
    config=Config(
        log_level=LogLevel.INFO,
        output="remote",
        remote_config=RemoteConfig(
            url="https://logs.example.com",
            headers={"Authorization": "Bearer your-token"}
        )
    )
)

@remote_logger.trace()
def important_function():
    # Function logic here
    pass
```

### Web UI Configuration

```python
from tracebook.config import WebUIConfig

web_logger = Logger(
    config=Config(
        log_level=LogLevel.INFO,
        output="both",
        web_config=WebUIConfig(
            title="My TraceBook Dashboard",
            foreground_color="#123456",
            background_color="#F0F0F0",
            show_star_on_github=True,
            indent_logs=True,
            is_active=True,
            port=2234,
            refresh_interval=2000,
            max_data_points=200,

        )
    )
)

@web_logger.trace()
def monitor_system():
    # Function logic here
    pass
```

### Configuring Log Levels and Output

Control the verbosity of logs by setting the log level and choosing the output:

```python
from tracebook import Logger
from tracebook.config import Config, LogLevel

logger = Logger(
    config=Config(
        log_level=LogLevel.DEBUG,
        output="both",
        file_path="logs.txt"
    )
)

@logger.trace(log_resources=True)
def my_function(param1, param2):
    return param1 + param2

my_function(1, 2)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
