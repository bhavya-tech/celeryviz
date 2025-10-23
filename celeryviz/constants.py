CLIENT_NAMESPACE = "/client"
SERVER_NAMESPACE = "/server"

DEFAULT_PORT = 9095
SOCKETIO_HOST_LOCATION = 'localhost'
SOCKETIO_HOST_URL = 'http://%s:%d' % (SOCKETIO_HOST_LOCATION,
                                           DEFAULT_PORT)

SOCKETIO_CLIENT_NAMESPACE_URL = 'http://%s%s' % (
    SOCKETIO_HOST_URL, CLIENT_NAMESPACE)

CELERY_DATA_EVENT = 'celery_events_data'

DEFAULT_LOG_FILE = './log.ndjson'
