# CeleryViz

> A UI-centric tool for visualising Celery task execution.

[![PyPI](https://img.shields.io/pypi/v/celeryviz?logo=pypi&logoColor=white)](https://pypi.org/project/celeryviz/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue?logo=apache&logoColor=white)](LICENSE)
[![Docs](https://img.shields.io/readthedocs/celeryviz?logo=readthedocs&logoColor=white)](https://celeryviz.readthedocs.io/)
[![Docker Image](https://img.shields.io/badge/docker-bhavyatech%2Fceleryviz-blue?logo=docker)](https://hub.docker.com/r/bhavyatech/celeryviz)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/bhavya-tech/celeryviz)



Debugging async Celery tasks usually means combing through log files. CeleryViz gives you a real-time visual trace of your task execution flow instead, so you can spot bottlenecks, failures, and task chains at a glance.


👉 **[Try the Live Demo](https://bhavya-tech.github.io/celeryviz_demo/)**

▶ **[Watch on YouTube](https://www.youtube.com/watch?v=ZXM--jIFfR8)**

📖 **[Read the Docs](https://celeryviz.readthedocs.io/)**

## Quick Start

Using Python library

```bash
pip install celeryviz
celery -A your_app celeryviz
```

Or using Docker image (with your existing Celery app)

```bash
docker pull bhavyatech/celeryviz:latest
docker run -p 9095:9095 -v $PWD:/app bhavyatech/celeryviz:latest celery -A your_app celeryviz
```

Or using Docker image (with broker URL)

```bash
docker pull bhavyatech/celeryviz:latest
docker run -p 9095:9095 bhavyatech/celeryviz:latest celery --broker='<broker_url>' celeryviz
```



Then open [http://localhost:9095/app/](http://localhost:9095/app/) in your browser.

📖 **[Full installation & setup guide →](https://celeryviz.readthedocs.io/en/latest/installation.html)**


## What it does

- **Visualises task flow:** See tasks, their states, and execution order in a clean UI
- **Real-time updates:** Watch tasks progress live as your workers process them
- **Zero code changes:** Plug in via CLI, works with your existing Celery app
- **Flexible deployment:** Run as a Python package or a Docker container


## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.  
For issues or feature requests, open a [GitHub Issue](https://github.com/bhavya-tech/celeryviz/issues).


## License

[Apache 2.0](LICENSE)


# Reporting violations

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement at [bhavyapeshavaria@gmail.com](mailto:bhavyapeshavaria@gmail.com). All complaints will be reviewed and investigated promptly and fairly.
