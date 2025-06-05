#####################################
# Docker stages for building the UI #
#####################################

# Run `docker build --target export --output ./celeryviz/static ./` to build the UI locally.

FROM instrumentisto/flutter:3 AS base

# Set the working directory inside the container
WORKDIR /app

# Pre-cache the Flutter SDK (this step will only run if the base image is updated)
RUN flutter precache

# Build stage
FROM base AS build

ARG SOURCE="main"
ARG GIT_REPO="https://github.com/bhavya-tech/celeryviz_with_lib.git"

RUN git clone $GIT_REPO
WORKDIR /app/celeryviz_with_lib
RUN git checkout $SOURCE

# Enable web support for Flutter
RUN flutter config --enable-web

# Now that the repo is cloned, we can run 'flutter pub get'
RUN flutter pub get

# Build the Flutter web app with CanvasKit renderer
RUN flutter build web --release

# Final stage: export the build files
# This is needed other wise all the linux files will be copied to the final image.
FROM scratch AS export
COPY --from=build /app/celeryviz_with_lib/build/web /
###########################################
###########################################



###########################################
# Docker stage for the Python application #
###########################################

FROM python:3.9

WORKDIR /app

COPY . .

# Build UI
COPY --from=export / /app/celeryviz/static/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir redis
RUN pip install .

# PYTHONUNBUFFERED: Force stdin, stdout and stderr to be totally unbuffered. (equivalent to `python -u`)
# PYTHONHASHSEED: Enable hash randomization (equivalent to `python -R`)
# PYTHONDONTWRITEBYTECODE: Do not write byte files to disk, since we maintain it as readonly. (equivalent to `python -B`)
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1

EXPOSE 9095

CMD ["celery", "celeryviz"]
