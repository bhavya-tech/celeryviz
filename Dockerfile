#########################################
# Docs                                  #
#########################################
# There are two ways to build the UI:
# 1. Download the prebuilt UI
#    a. If you want to build complete image with prebuilt UI, use the `celeryviz` target.
#       Run: `docker build --target celeryviz`
#    b. If you want to download only the prebuilt UI, use the `prebuilt` target.
#       Run: `docker build --target webapp-prebuilt --output . .`
# 2. Build from source
#    a. If you want to build complete image from source, use the `celeryviz-with-frontend-build` target.
#       Run: `docker build --target celeryviz-with-frontend-build`
#    b. If you want to build only the UI, use the `webapp-build` target.
#       Run: `docker build --target webapp-build --output . .`
#    - The `GIT_REPO` and `SOURCE` build args can be passed for specific builds.
#########################################


#####################################
# Docker stages for building the UI #
#####################################
FROM instrumentisto/flutter:3 AS flutter_build_base

# Set the working directory inside the container
WORKDIR /app

# Pre-cache the Flutter SDK (this step will only run if the base image is updated)
RUN flutter precache

# Build stage
FROM flutter_build_base AS webapp-compile

ARG SOURCE="main"
ARG GIT_REPO="https://github.com/bhavya-tech/celeryviz_with_lib.git"

RUN git clone $GIT_REPO
WORKDIR /app/celeryviz_with_lib
RUN git checkout $SOURCE

# Enable web support for Flutter
RUN flutter config --enable-web
RUN flutter pub get
RUN flutter build web --release

# Use this stage if static files are needed in the actual folder structure.
FROM scratch AS webapp-build
COPY --from=webapp-compile /app/celeryviz_with_lib/build/web /celeryviz/static/
###########################################
###########################################


################################################
# Docker stage to download the prebuilt webapp #
################################################

# Download and extract the prebuilt webapp
# This is needed for users who do not want to build the webapp from source.
FROM alpine:3.14 AS download-and-extract-prebuilt
ARG FRONTEND_VERSION="latest"
RUN apk add --no-cache unzip curl && mkdir /app/
RUN if [ "$FRONTEND_VERSION" = "latest" ]; then \
        curl -L -o /app/webapp-build.zip \
            https://github.com/bhavya-tech/celeryviz_with_lib/releases/latest/download/webapp-build.zip; \
    else \
        curl -L -o /app/webapp-build.zip \
            https://github.com/bhavya-tech/celeryviz_with_lib/releases/download/$FRONTEND_VERSION/webapp-build.zip; \
    fi

RUN unzip /app/webapp-build.zip -d /app/static && \
    rm /app/webapp-build.zip

# Use this stage if static files are needed in the actual folder structure.
FROM scratch AS webapp-prebuilt
COPY --from=download-and-extract-prebuilt /app/static/ /celeryviz/static/
###########################################
###########################################


###########################################
# Docker stage for the Python application #
###########################################

FROM python:3.9-alpine AS setup-celeryviz-dependency

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir redis 

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
# PYTHONDONTWRITEBYTECODE: Do not write byte files to disk, since we maintain it as readonly. (equivalent to `python -B`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
EXPOSE 9095
###########################################
###########################################


#######################
# Final docker stages #
#######################

# This stage builds celeryviz with the frontend built from the source.
FROM setup-celeryviz-dependency AS celeryviz-with-frontend-build
COPY --from=webapp-compile /app/celeryviz_with_lib/build/web /app/celeryviz/static/
RUN pip install .

# This stage builds celeryviz with the prebuilt frontend.
FROM setup-celeryviz-dependency AS celeryviz
COPY --from=download-and-extract-prebuilt /app/static/ /app/celeryviz/static/
RUN pip install .

