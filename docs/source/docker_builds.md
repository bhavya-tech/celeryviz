# Docker Build Stages & Targets

The `celeryviz` Dockerfile uses a multi-stage build process to optimize image size and provide flexibility in how the application and its frontend are built.

## Overview of Build Stages

The build process is divided into three main flows:
1. **Building from source**: Compiling the Flutter web application from given source.
2. **Using prebuilt Frontend**: Downloading a pre-compiled version of the frontend.
3. **Setting up Celeryviz**: Setting up the Python application and dependencies.

### Final Build Targets

1. `celeryviz`: To build the docker image with prebuilt frontend.
2. `celeryviz-with-frontend-build`: To build the docker image with frontend compiles from source.
3. `webapp-prebuilt`: To populate the `celeryviz/static` folder with latest prebuilt frontend. (To be used for development)
4. `webapp-build`: To populate the `celeryviz/static` folder with frontend built from source. (To be used for development)

**Custom Build Arguments:**

- `--build-arg SOURCE`: Specify a different branch, tag, or commit hash.
- `--build-arg GIT_REPO`: Specify a different repository URL (e.g., your own fork).

These build arguments will take effect for the build stages `celeryviz-with-frontend-build` and `webapp-build`.

### Build Stages Dependency Graph

![Build Stages Dependency Graph](../media/CeleryvizDockerStagesVisualization.png)

### Example: Building from a specific feature branch

  - Build the docker image with frontend compiled from source
```bash
docker build --target celeryviz-with-frontend-build \
    --build-arg SOURCE="feature/new-ui" \
    --build-arg GIT_REPO="https://github.com/your-username/celeryviz_with_lib.git" \
    -t celeryviz:custom .
```

  - Compile your own frontend and populate the `celeryviz/static` folder.
```bash
docker build --target webapp-build \
    --build-arg SOURCE="feature/new-ui" \
    --build-arg GIT_REPO="https://github.com/your-username/celeryviz_with_lib.git" \
    --output . .
```
