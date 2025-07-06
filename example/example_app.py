from time import sleep
import celery
from celeryviz.log import attach_log_sender

app = celery.Celery('example_app', broker='redis://redis:6379/0')
logger = celery.utils.log.get_task_logger(__name__)

attach_log_sender(app, logger)

@app.task
def add(x, y, z=0):

    sleep(3)
    add.apply_async(args=[x+1, y+100], kwargs={'z': z+10000}, countdown=5)
    
    sleep(3)
    logger.info("Adding %s + %s + %s." % (x, y, z))

    sleep(3)
    return x + y + z

app.register_task(add)