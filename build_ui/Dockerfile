# Use the official Flutter Docker image as the base
FROM instrumentisto/flutter AS base

# Set the working directory inside the container
WORKDIR /app

# Pre-cache the Flutter SDK (this step will only run if the base image is updated)
RUN flutter precache

# Build stage
FROM base AS build

ARG GITHUB_PAT=""
ARG SOURCE="main"
ARG GIT_REPO="https://github.com/bhavya-tech/celeryviz_with_lib.git"

# Clone the repository and checkout the specified branch
# Do a fake operation with time so that cache is invalidated


# Uncomment the below once the repo is public. This will only invlaidate cache if there
# is a new commit in the repo. This will be the perfect solution. 
# ADD "https://api.github.com/repos/bhavya-tech/celeryviz/commits?per_page=1" latest_commit
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

RUN if [ $GITHUB_PAT != "" ]; then git config --global url."https://${GITHUB_PAT}@github.com/".insteadOf "https://github.com/"; fi
RUN git clone $GIT_REPO

WORKDIR /app/celeryviz_with_lib
RUN git checkout $SOURCE

# Enable web support for Flutter
RUN flutter config --enable-web

# Now that the repo is cloned, we can run 'flutter pub get'
RUN flutter pub get

# Build the Flutter web app using CanvasKit renderer
RUN flutter build web --web-renderer canvaskit --release

# Final stage: export the build files
FROM scratch AS export
COPY --from=build /app/celeryviz_with_lib/build/web /
