# Use the official Flutter Docker image as the base
FROM instrumentisto/flutter AS base

# Set the working directory inside the container
WORKDIR /app

# Pre-cache the Flutter SDK (this step will only run if the base image is updated)
RUN flutter precache

# Build stage
FROM base AS build

ARG SOURCE="main"
ARG GIT_REPO="https://github.com/bhavya-tech/celeryviz_with_lib.git"

# Clone the repository and checkout the specified branch

# is a new commit in the repo. This will be the perfect solution. 
ADD "https://api.github.com/repos/bhavya-tech/celeryviz/commits?per_page=1" latest_commit

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
FROM scratch AS export
COPY --from=build /app/celeryviz_with_lib/build/web /






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

# Expose the port the app runs on
EXPOSE 9095

CMD ["celery", "celeryviz"]
