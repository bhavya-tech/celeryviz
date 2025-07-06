CeleryViz
=========

A UI centric tool for visualising Celery task execution.

[**Live Demo**](https://bhavya-tech.github.io/celeryviz_demo/)

<video src="https://github.com/user-attachments/assets/ec6b0f0e-2ad6-4a2c-8928-a7765fd96023"></video>


This project simplifies debugging of asynchronous Celery tasks by offering a visual representation of the task execution flow. Instead of combing through the log files, developers can use Celeryviz to visually trace and debug task processes more efficiently.

## Installation

1. Python library

```bash
pip install celeryviz
```

2. Docker image
```bash
docker pull bhavyatech/celeryviz:0.0.3
```

## Run the example
  - To test the example, you can use the provided Docker Compose setup. This will set up a Redis server, a Celery worker, and the CeleryViz server.
```bash
cd example
docker-compose up --build
```
(This may take a few minutes to build the first time.)

## Usage

#### 1. Create a celery project.
  - Use [this gist](https://gist.github.com/bhavya-tech/d937ef45905720014ee12fe332352966) for a minimal example.

```bash
curl https://gist.githubusercontent.com/bhavya-tech/d937ef45905720014ee12fe332352966/raw/0afac784adfb6b407fa83ce4b19e6f3cab4d80d9/example_app.py -o example_app.py
```

#### 2. Start the celery worker:

  - Ensure a message broker is running (can use [RabbitMQ](https://www.rabbitmq.com/docs/download) for simplicity)

  - Schedule a task for celery to run:

```bash
celery -A example_app call example_app.add --args='[1, 100]' --kwargs='{"z":10000}'
```

  - Run the celery worker.
```bash
celery -A example_app worker -l info -E
```

#### 3. Start the CeleryViz server:

##### 3.1 Using docker image
There are two ways to run celeryviz:

  1. Pass the broker url 
```bash
docker run -p 9095:9095 bhavyatech/celeryviz:0.0.3 celery --broker='<broker_url>' celeryviz
```

  2. Use the configuration of [celery application](https://docs.celeryq.dev/en/stable/userguide/application.html).
```bash
docker run -p 9095:9095 -v $PWD:/app bhavyatech/celeryviz:0.0.3 celery -A example_app.app celeryviz
```


##### 3.2 Using the installed celeryviz python library
  - In a new terminal, run the following command:

```bash
celery -A example_app celeryviz
```

#### 4. Connect to the server:
  -  Open your browser and go to [http://localhost:9095/app/]()

---

# Reporting violations

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement at [bhavyapeshavaria@gmail.com](mailto:bhavyapeshavaria@gmail.com). All complaints will be reviewed and investigated promptly and fairly.
