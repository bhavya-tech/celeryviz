# Usage & Examples

## Quick Start

### 1. Start your Celery Worker

Ensure your worker is started with events enabled (`-E` flag):

```bash
celery -A your_app worker -l info -E
```

### 2. Start CeleryViz

Run the `celeryviz` command to start the monitoring server:

```bash
celery -A your_app celeryviz
```

If you don't want to couple your celery app with celeryviz, you can pass the broker url directly:

```bash
celery --broker='amqp://guest@localhost//' celeryviz
```

### 3. View the Visualization

Open your browser and navigate to:
[http://localhost:9095/app/](http://localhost:9095/app/)


## Docker Usage

`celeryviz` is available as a pre-built Docker image, making it easy to run in containerized environments.

### Pulling the Image

You can pull the latest version from Docker Hub:

```bash
docker pull bhavyatech/celeryviz:latest
```

### Running with a Broker URL

The simplest way to run the image is by passing the broker URL directly:

```bash
docker run -p 9095:9095 bhavyatech/celeryviz:latest celery --broker='<broker_url>' celeryviz
```

### Running with a Celery App

If you have a Celery application, you can mount your project directory and point to your app:

```bash
docker run -p 9095:9095 -v $PWD:/app bhavyatech/celeryviz:latest celery -A your_app_module celeryviz
```
