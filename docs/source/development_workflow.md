# Development Workflow

This page provides an in-depth look at the local development workflow for `celeryviz`, complementing the basic [Setup Guide](dev_environment).

## Development Philosophy

`celeryviz` is designed to be developed iteratively. Since the frontend is a separate Flutter project and the backend is a Python application, we use several strategies to keep development fast.

## Backend Development

The backend is a Celery command. When developing:

1. **Editable Installation**: Always install the package in editable mode:
   ```bash
   pip install -e .
   ```
2. **Auto-Reloading**: While Celery doesn't natively support auto-reload for custom commands, you can use helpers like `watchdog` to restart the server on file changes.
3. **Environment Variables**: Use a `.env` or `config.env` file to manage local settings like `CELERYVIZ_PORT`.

## Frontend Integration

The backend serves static files from `celeryviz/static/`. 

- **Prebuilt Frontend**: For most backend-only development, use `webapp-prebuilt` to quickly populate the `static/` folder.
- **Custom Frontend**: If you are modifying the UI, you will need to build it using the Flutter SDK and copy the results into `celeryviz/static/`.

## Using Docker for Development

The `Dockerfile` is an essential part of the development workflow.

### Testing Full Builds
To ensure your changes work in a production-like container:
```bash
docker build --target celeryviz -t celeryviz:local .
```

### Building with Custom Frontend Branches
If you are working on a frontend feature branch simultaneously:
```bash
docker build --target celeryviz-with-frontend-build \
    --build-arg SOURCE="your-branch-name" \
    -t celeryviz:frontend-dev .
```

## Continuous Integration

Every pull request should pass:
1. **Unit Tests**: Run `pytest`.
2. **Build Test**: Ensure the Docker image builds successfully.
3. **Documentation Build**: Ensure `make html` in the `docs/` directory produces no errors.
