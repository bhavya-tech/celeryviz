import logging

import click
from celery.bin.base import CeleryCommand

from .constants import DEFAULT_LOG_FILE
from .executor import starter

LOGGING_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

logger = logging.getLogger(__name__)

def set_log_level(log_level):
    logging.basicConfig(level=logging.CRITICAL)
    logger = logging.getLogger(__package__)
    logger.setLevel(LOGGING_LEVELS[log_level])


@click.command(cls=CeleryCommand,
               context_settings={
               'ignore_unknown_options': True})
@click.option('--record',
              default=False,
              is_flag=True)
@click.option('-l', '--log-level',
              default='INFO',
              type=click.Choice(LOGGING_LEVELS.keys(),
                                case_sensitive=False))
@click.option('--file',
              default=DEFAULT_LOG_FILE,
              type=click.Path())
@click.pass_context
def celeryviz(ctx, record, log_level, file):
    set_log_level(log_level)
    starter(ctx, record, file)
