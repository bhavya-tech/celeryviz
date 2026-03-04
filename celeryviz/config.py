import os
from types import SimpleNamespace
from .constants import DEFAULT_PORT

class Settings(SimpleNamespace):
    port = DEFAULT_PORT
    log_level = 'INFO'
    record_file = None
    no_socketio = False

settings = Settings()
