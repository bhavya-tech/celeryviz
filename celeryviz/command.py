import click
from celery.bin.base import CeleryCommand

from .constants import DEFAULT_LOG_FILE
from .executor import starter


@click.command(cls=CeleryCommand, context_settings={
    'ignore_unknown_options': True
})
@click.option('--record', default=False, is_flag=True)
@click.option('--file', default=DEFAULT_LOG_FILE, type=click.Path())
@click.pass_context
def celeryviz(ctx, record, file):
    starter(ctx, record, file)
