# Trace Book

**Trace Book** is a Python package designed for comprehensive code bookkeeping. It provides tools to log function calls, parameters, return values, and execution times. Additionally, it supports decorators for easy integration, automatic error tracking, and remote log transmission, all with customizable log levels and output configurations.

## Features

- **Function Logging**: Track function calls, parameters, return values, and execution times.
- **Automatic Error Tracking**: Log exceptions and stack traces automatically.
- **Decorators**: Simplify logging with decorators that track function parameters and results.
- **Remote Log Transmission**: Securely send logs to a remote server.
- **Customizable Log Levels**: Control log verbosity with DEBUG, INFO, WARNING, and ERROR levels.
- **Configurable Output**: Choose between logging to files or transmitting logs to a remote server.

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

To log function calls, parameters, return values, and execution times, you can use the logging functionality:

```python
from tracebook import Logger
from tracebook.config import Config, LogLevel

logger = Logger(
    config=Config(log_level=LogLevel.INFO, output="both", file_path="test.log")
)

@logger.trace(log_resources=True)
def fact(x):
    if x == 0:
        return 1
    else:
        return x * fact(x - 1)

@logger.trace(log_resources=True)
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

@logger.trace(log_resources=True)
def complex_operation(x):
    fact_result = fact(x)
    fib_result = fibonacci(x)
    return fact_result + fib_result

if __name__ == "__main__":
    while True:
        x = int(input("Enter a number: "))
        result = complex_operation(x)
        print(f"Result of complex operation with {x}: {result}")
```

### Using Decorators

To simplify logging, you can use the provided decorators:

```python
from tracebook import Logger
from tracebook.config import Config, LogLevel

logger = Logger(
    config=Config(log_level=LogLevel.INFO, output="both", file_path="test.log")
)

@logger.trace(log_resources=True)
def my_function(param1, param2):
    return param1 + param2

my_function(1, 2)
```

### Remote Log Transmission

To send logs to a remote server, configure the remote settings in `Config`:

```python
from tracebook import Logger
from tracebook.config import Config, LogLevel, RemoteConfig

logger = Logger(
    config=Config(
        log_level=LogLevel.INFO,
        output="file",
        file_path="test.log",
        remote_config=RemoteConfig(
            url="https://yourserver.com/log",
            headers={"Authorization": "Bearer yourapikey"}
        )
    )
)

@logger.trace(log_resources=True)
def my_function(param1, param2):
    return param1 + param2

my_function(1, 2)
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

## Documentation

For more detailed documentation, including advanced usage, configuration options, and examples, please refer to the `docs/` directory or visit the online documentation at [https://yourdocslink.com](https://yourdocslink.com).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
