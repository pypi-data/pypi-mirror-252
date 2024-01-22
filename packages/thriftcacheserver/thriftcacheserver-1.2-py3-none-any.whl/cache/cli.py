from cache.server import server
from cache.client.python import client
import click


@click.group()
def cli():
    pass


@cli.command()
def run_server():
    server.main()


@cli.command()
def run_client():
    client.main()


def main():
    cli()
