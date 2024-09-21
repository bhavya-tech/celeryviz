CeleryViz
=========

A tool for visualising execution of Celery tasks.

<video src="https://github.com/user-attachments/assets/ec6b0f0e-2ad6-4a2c-8928-a7765fd96023"></video>


## Installation

```bash
pip install celeryviz
```

## Usage

#### 1. Create a celery project.
  - Use [this gist](https://gist.github.com/bhavya-tech/d937ef45905720014ee12fe332352966) for a minimal example.

#### 2. Start the celery worker:

```bash
celery -A example_app worker
```

#### 3. Start the CeleryViz server:

```bash
celery -A example_app celeryviz
```

  -  Open your browser and go to [http://localhost:5000/]()

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

