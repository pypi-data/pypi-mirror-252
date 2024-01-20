# Moonhub Logger

The `mh_logger` handles logging into GCP and locally in a seamless manner.

## Installation

```
python3 -m pip install mh_logger
```

## User guide

### Basic log

A basic log is composed of a message and kwargs to be logged.

```
from mh_logger import LoggingManager
logger = LoggingManager(__name__)
logger.info("This is a sample log", foo="bar")
```
Output:
```
2023-03-16 20:22:36,561 [INFO] - Test: This is a sample log - JSON Payload: {
    'foo': 'bar',
    "_message": "This is a sample log",
    "request_id": "b30cb564210a4172b00d273ad441f9e2"
}
```

### Binded variables

Binded variables are variables preserved across different modules and functions within the same thread (from the `threading` module) or within the same Task (from the `asyncio` module). Example:

```
logger.bind(foo="bar", hello="world")

def a():
    logger.info("My first log")

def b():
    logger.info("My second log")

a()
b()
```
Output:
```
2023-03-16 20:22:36,561 [INFO] - Test: My first log - JSON Payload: {
    "foo": "bar",
    "hello": "world",
    "_message": "My first log",
    "request_id": "b30cb564210a4172b00d273ad441f9e2"
}
2023-03-16 20:22:37,561 [INFO] - Test: My second log - JSON Payload: {
    "foo": "bar",
    "hello": "world",
    "_message": "My second log",
    "request_id": "b30cb564210a4172b00d273ad441f9e2"
}
```

### The `request_id`

The `request_id` or `logger_id` is a special binded variable added by default to all logs.

### Multi threading

We must explicitly propagate the binded variables (including the `request_id`) to other threads. Example:

```
logger.info("Log on the main thread")
with ThreadPoolExecutor(
    initializer=logger.bind, initargs=(logger.binded,)
) as executor:
    executor.submit(logger.info, "Log on a different thread")
```
Output:
```
2023-03-16 20:22:36,561 [INFO] - Test: Log on the main thread - JSON Payload: {
    "_message": "Log on the main thread",
    "request_id": "b30cb564210a4172b00d273ad441f9e2"
}
2023-03-16 20:22:37,561 [INFO] - Test: Log on a different thread - JSON Payload: {
    "_message": "Log on a different thread",
    "request_id": "b30cb564210a4172b00d273ad441f9e2"
}
```

## Contribute to the Moonhub Logger

Set following environment variable if you want to push logs to GCP Cloud Logging service while testing locally.
```
GCP_SERVICE_KEY=google-service-key.json
```

## Deploy to pypi

https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives

You will need to add `--skip-existing`.
