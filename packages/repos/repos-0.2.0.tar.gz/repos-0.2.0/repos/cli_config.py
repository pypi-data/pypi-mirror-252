import click


@click.group()
def config():
    """Manages repos config"""


@config.command()
@click.argument("repo", type=str, nargs=-1)
def ls(repo):
    """Shows the config for repos"""
    print(f"Config json: {repo}")


@config.command()
@click.argument("name", type=str, required=True)
@click.argument("value", required=True)
@click.argument("repo", type=str, nargs=-1)
def set(repos, value):
    """Saves a config repos"""
    print(f"Setting {name}: {value} in {repo}")


@config.command()
@click.argument("name", type=str, required=True)
@click.argument("repo", type=str, nargs=-1)
def rm(repos, value):
    """Removes a config in repos"""
    print(f"Setting {name}: {value} in {repo}")
