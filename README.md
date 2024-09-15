CeleryViz
=========

A tool for visualising execution of Celery tasks.

# Getting started

## Installation

```bash
pip install celeryviz
```

## Usage

  - First start the celery worker:

```bash
celery -A proj worker
```
(`proj` is the name of your Celery project)

  - Then start the CeleryViz server:


```bash
celery -A proj celeryviz
```

  - Open your browser and go to [http://localhost:3000/]()

## Preview


# Contributing

## Getting started
1. Clone this repository.

2. Build the webapp.

The UI webapp is maintained separately in Flutter. 

Run the following command to build the latest version of standard webapp locally (ensure that docker is installed):

```bash
docker build --output ./celeryviz/static ./build_ui
```

For customised builds, the following build args can be used:

Args for docker build:
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

3. Install the package in editable mode:

```bash
pip install -e .
```

