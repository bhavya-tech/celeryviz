from types import SimpleNamespace
from .constants import DEFAULT_PORT

class Settings(SimpleNamespace):
    port = DEFAULT_PORT
    log_level = 'INFO'
    record_file = None
    no_socketio = False
    clickhouse_enable = False
    clickhouse_host = None
    clickhouse_port = 8123
    clickhouse_database = 'default'
    clickhouse_username = None
    clickhouse_password = ''
    clickhouse_file_path = None
    clickhouse_engine = 'Memory'

    def update_from_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_dict(self):
        return self.__dict__

settings = Settings()
