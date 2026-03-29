# Installation & Configuration

## Prerequisites

- Python 3.8+
- A running Celery project
- A message broker (Redis, RabbitMQ, etc.)

## Installation

You can install `celeryviz` directly from PyPI:

```bash
pip install celeryviz
```

Or using docker image:

```bash
docker pull bhavyatech/celeryviz:latest
```

## Configuration

### Celeryviz Configuration
`celeryviz` can be configured via environment variables or passing arguments to the command line.

| CLI Argument | Environment Variable | Description | Default |
|----------|-------------|---------|---------|
| `--port`, `-p` | `CELERYVIZ_PORT` | Port for the visualization server | `9095` |
| `--no-socketio` | `CELERYVIZ_NO_SOCKETIO` | Disable live streaming of events through socketio (to be used when only recording to file or dumping to DB) | `False` |
| `--record-file` | `CELERYVIZ_RECORD_FILE` | Path to the log file to record events to. (.jsonl or .ndjson only accepted) | `None` |
| `--log-level`, `-l` | `CELERYVIZ_LOG_LEVEL` | Log level for the visualization server | `INFO` |

### Celery Configuration
Apart from the provided config, the standard celery configuration is also supported by passing those before `celeryviz` sub-command.

### Example
1. Using `-A` flag to use celery app configuration

```bash
celery -A your_app_name celeryviz -l INFO --record-file=./events.jsonl
```

2. Using `--broker` flag to use directly connect to broker rather than a celery app configuration

```bash
celery --broker='redis://host.docker.internal:6379/0' -A celeryviz -l INFO --record-file=./events.jsonl
```
