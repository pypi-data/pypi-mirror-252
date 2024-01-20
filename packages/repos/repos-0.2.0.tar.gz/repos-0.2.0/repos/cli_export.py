import click


@click.group()
def export():
    """Exports the repos"""


@export.command()
@click.argument("repos", type=str, nargs=-1)
def json(repos):
    """Exports the repos as json"""
    print(f"Export json: {repos}")


@export.command()
@click.argument("repos", type=str, nargs=-1)
def yaml(repos):
    """Exports the repos as yaml"""
    print(f"Export yaml: {repos}")
