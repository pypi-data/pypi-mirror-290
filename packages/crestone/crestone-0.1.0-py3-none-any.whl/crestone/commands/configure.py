import click

@click.command()
@click.option('--cloud', type=click.Choice(['aws', 'azure', 'gcp']), required=True)
def configure(cloud):
    click.echo(f"Configuring Crestone for {cloud}")