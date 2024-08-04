import logging

import celery
from celery.app import Celery


def attach_log_sender(app: Celery, logger):

    if not hasattr(logger, 'handlers'):
        raise ValueError('logger must support handlers to send logs')
    
    log_level = getattr(logger, 'level', logging.NOTSET)

    handler = TaskLogEmitter(app, level=log_level)
    logger.addHandler(handler)


class TaskLogEmitter(logging.Handler):
    def __init__(self, app: Celery, level=logging.NOTSET):
        self.app = app
        super(TaskLogEmitter, self).__init__(level=level)

    def emit(self, record):
        with self.app.events.default_dispatcher() as d:
            d.send('task-log', uuid=celery.current_task.request.id, msg=record.getMessage(), levelno=record.levelno,
                   pathname=record.pathname, lineno=record.lineno, name=record.name,  exc_info=record.exc_info)
