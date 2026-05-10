import logging

import click
from celery.bin.base import CeleryCommand

from .config import settings
from .constants import DEFAULT_PORT
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

@click.option('-l', '--log-level',
              default='INFO',
              envvar='CELERYVIZ_LOG_LEVEL',
              type=click.Choice(list(LOGGING_LEVELS.keys()),
                                case_sensitive=False))
@click.option('--record-file',
              envvar='CELERYVIZ_RECORD_FILE',
              help='Path to the log file to record events to. (.jsonl or .ndjson only accepted)',
              type=click.Path())

@click.option('--no-socketio',
              is_flag=True,
              envvar='CELERYVIZ_NO_SOCKETIO',
              help='Disable Socket.IO event support.')

@click.option('-p', '--port',
              default=DEFAULT_PORT,
              envvar='CELERYVIZ_PORT',
              type=int,
              help=f'Port to run the web server on (default: {DEFAULT_PORT})')

@click.option('--clickhouse-enable',
              is_flag=True,
              help='Enable ClickHouse event sink.')

@click.option('--clickhouse-host',
              default=None,
              help='ClickHouse host address (default: localhost)')

@click.option('--clickhouse-port',
              default=8123,
              type=int,
              help='ClickHouse HTTP port (default: 8123)')

@click.option('--clickhouse-database',
              default='default',
              help='ClickHouse database name (default: default)')

@click.option('--clickhouse-username',
              default=None,
              help='ClickHouse username (default: None)')

@click.option('--clickhouse-password',
              default='',
              help='ClickHouse password (default: empty string)')

@click.option('--clickhouse-file-path',
              help='File path for ClickHouse chDB file engine.')

@click.option('--clickhouse-engine',
              type=click.Choice(['MergeTree', 'Memory', 'File']),
              default='Memory',
              help='ClickHouse table engine. MergeTree will connect to hosted DB, Memory and File for local testing.')

@click.pass_context
def celeryviz(ctx, **kwargs):
    settings.update_from_kwargs(**kwargs)

    set_log_level(settings.log_level)
    starter(ctx)
