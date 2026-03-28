# Development Environment Setup

This guide explains how to set up a local development environment for `celeryviz`.

## Prerequisites

- Python 3.8 or higher
- `pip` and `virtualenv` (or `venv`)
- A running Redis or RabbitMQ instance for testing

## Setting up the environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bhavya-tech/celeryviz.git
   cd celeryviz
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   Install the package in editable mode along with development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```

## Running Tests

We use `pytest` for testing. You can run the test suite using:

```bash
pytest
```

## Testing the frontend with an example celery application

The `example` folder contains a sample celery application that can be used to test the application. It uses docker compose to set up the environment and build the local celeryviz docker image.

```bash
cd example
docker-compose up --build
```

Note: It does not watch the fiels for changes, so it needs to be rebuilt after changes. To get around this, you can run the celeryviz server with [watchdog](https://pypi.org/project/watchdog/) and use the redis and celery worker from the docker containers.

## Building Documentation Locally

To build and view the documentation:

```bash
cd docs
make html
# Then open build/html/index.html in your browser
```
