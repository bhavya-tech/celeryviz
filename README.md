CeleryViz
=========

A UI centric tool for visualising Celery task execution.

[**Live Demo**](https://bhavya-tech.github.io/celeryviz_demo/)

<video src="https://github.com/user-attachments/assets/ec6b0f0e-2ad6-4a2c-8928-a7765fd96023"></video>


This project simplifies debugging of asynchronous Celery tasks by offering a visual representation of the task execution flow. Instead of combing through the log files, developers can use Celeryviz to visually trace and debug task processes more efficiently.

## Installation

```bash
pip install celeryviz
```

## Usage

#### 1. Create a celery project.
  - Use [this gist](https://gist.github.com/bhavya-tech/d937ef45905720014ee12fe332352966) for a minimal example.

```bash
curl https://gist.githubusercontent.com/bhavya-tech/d937ef45905720014ee12fe332352966/raw/0afac784adfb6b407fa83ce4b19e6f3cab4d80d9/example_app.py -o example_app.py
```

#### 2. Start the celery worker:

  - Ensure a message broker is running (can use [RabbitMQ](https://www.rabbitmq.com/docs/download) for simplicity)

```bash
celery -A example_app worker
```

#### 3. Start the CeleryViz server:

```bash
celery -A example_app celeryviz
```

  -  Open your browser and go to [http://0.0.0.0:9095/app/]()

---

# Reporting violations

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement at [bhavyapeshavaria@gmail.com](mailto:bhavyapeshavaria@gmail.com). All complaints will be reviewed and investigated promptly and fairly.
