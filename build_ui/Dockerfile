FROM instrumentisto/flutter AS build

WORKDIR /app
ARG GITHUB_PAT
RUN git config --global url."https://${GITHUB_PAT}@github.com/".insteadOf "https://github.com/"

RUN git clone https://github.com/bhavya-tech/celeryviz_with_lib.git
WORKDIR /app/celeryviz_with_lib

# Ensure Flutter is up to date and enable web support
RUN flutter config --enable-web

# Install Flutter dependencies
RUN flutter pub get

# Build the Flutter web app with CanvasKit renderer
RUN flutter build web --web-renderer canvaskit --release

FROM scratch AS export
COPY --from=build /app/celeryviz_with_lib/build/web /