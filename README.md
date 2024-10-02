CeleryViz
=========

A tool for visualising execution of Celery tasks.

[**Live Demo**](https://bhavya-tech.github.io/celeryviz_demo/)

![demo](https://github.com/user-attachments/assets/67d1b4a3-653a-43da-8028-a8437424f70a)


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

  - The `attach_log_sender` in the example gist sends logs to CeleryViz.
    - If a custom logger does not support handlers, then monkeypatch the logger to mimic the `attach_log_sender` function.

# Contributing

## Setting up the development environment
#### 1. Clone this repository.
```bash
git clone https://github.com/bhavya-tech/celeryviz.git
```

#### 2. Build the webapp

  - The UI webapp is maintained separately in [celeryviz_with_lib](https://github.com/bhavya-tech/celeryviz_with_lib).

  - Run the following command to build the latest version of standard webapp locally (ensure that [docker](https://www.docker.com/) is installed):

```bash
docker build --output ./celeryviz/static ./build_ui
```

For customised builds, the following optional build args can be used:
- `GITHUB_PAT`
    - If any of dependency repo is private, add a github personal access token as a build argument.
- `GIT_REPO`
    - The URL of the repository to build.
    - Defaults to [bhavya-tech/celeryviz_with_lib](https://github.com/bhavya-tech/celeryviz_with_lib.git)
- `SOURCE`
    - The branch of the repository to build. Default is `main`.
    - A particular commit hash can also be used.

```bash
docker build --output ./celeryviz/static --build-arg="GITHUB_PAT=<your github personal access token>" ./build_ui
```

#### 3. Install the package in editable mode:

```bash
pip install -e .
```

