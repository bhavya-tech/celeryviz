# Integration Guide

This `celeryviz` python package is a part of `celeryviz` suite and is designed to work with frontends and other tools in the ecosystem.

## Packaged Frontend

Most users will use the pre-packaged frontend included with this library. It is served automatically at `/app/` when the server is running.
[http://localhost:9095/app/](http://localhost:9095/app/)

## Celeryviz Desktop Application

This app is still under development. Users will be able to directly provide the url to the hosted instance of this library.

## Implementing your own frontend using `celeryviz_frontend_core`

The backend provides a REST API that the `celeryviz_frontend_core` consumes. If you are building a custom frontend:
1. Ensure your frontend can reach the `celeryviz` server port.
2. Use the available WebSocket or polling endpoints to receive task updates.