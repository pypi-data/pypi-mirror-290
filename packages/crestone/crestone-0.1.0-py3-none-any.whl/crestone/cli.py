import click
from .commands import configure, run, deploy

@click.group()
def cli():
    pass

cli.add_command(configure.configure)
cli.add_command(run.run)
cli.add_command(deploy.deploy)

if __name__ == '__main__':
    cli()