# Overview

`celeryviz` is a UI-centric tool designed to simplify the debugging of asynchronous Celery tasks by offering a visual representation of the task execution flow.

## Architectural Role

`celeryviz` acts as a monitoring layer that intercepts Celery events and provides a real-time visualization of task lifecycles. It is designed to be:
- **Lightweight**: Minimal overhead on your existing Celery workers.
- **Visual**: Replaces log-combing with interactive diagrams.
- **Extensible**: Integrates with the broader `celeryviz` suite.

## Suite Integration

This library is part of the `celeryviz` suite, which includes:
- `celeryviz`: The Python backend and event receiver (this project).
  - This library also packs a simple frontend for quick use.
- `celeryviz_frontend_core`: The core logic for the frontend visualization.
- Demo applications and packaged frontends for various environments.
- Celeryviz desktop application (to be launched soon)

By integrating these components, developers gain a comprehensive view of their distributed task execution environment.
