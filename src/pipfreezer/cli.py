import json
import logging

import click  # https://click.palletsprojects.com/

from .console import print_not_installed_packages
from .console import print_updated_packages
from .pipfreezer import find_requirements_files
from .pipfreezer import get_package_data_from_requirements
from .pipfreezer import get_pip_dict
from .pipfreezer import get_pip_list_as_json
from .pipfreezer import get_pip_list_outdated_as_json
from .pipfreezer import update_requirements_file
from .pipfreezer import upgrade_outdated_packages

logger = logging.getLogger(__name__)


def silent_echo(*args, **kwargs):
    pass


def common_options(func):
    """Decorator to add common options to a command."""
    # func = click.option(
    #     "-p",
    #     "--path",
    #     required=True,
    #     type=click.Path(),
    #     help="Path to the .env file or a directory containing .env files.",
    # )(func)
    return click.option("--verbose", is_flag=True, help="Enables verbose mode.")(func)


@click.command()
@common_options
def freeze(verbose) -> None:  # pragma: no cover
    """Main program."""

    if not verbose:
        click.echo = silent_echo

    package_dict = get_pip_dict(get_pip_list_as_json())
    requirements_files = find_requirements_files()

    updated = []
    not_installed = []
    for file in requirements_files:
        list1, list2 = update_requirements_file(file, package_dict)
        updated += list1
        not_installed += list2

    if updated:
        print_updated_packages(updated)

    if not_installed:
        print_not_installed_packages(not_installed)


@click.command()
@common_options
def upgrade(verbose) -> None:  # pragma: no cover
    """Upgrade outdated packages."""

    if not verbose:
        click.echo = silent_echo

    reqs = get_package_data_from_requirements()
    outdated_packages = json.loads(get_pip_list_outdated_as_json())

    to_install = [
        f"{pkg['name']}=={pkg['latest_version']}"
        for pkg in outdated_packages
        if any(pkg["name"] == req.name for req in reqs)
    ]

    if to_install:
        output = upgrade_outdated_packages(to_install)
        print(output)  # noqa: T201


# Set up your command-line interface grouping
@click.group()
@click.version_option()
def cli():
    """Pip Freezer pins packages no matter which requirements file they live
    in and maintains your comments and line breaks."""


cli.add_command(freeze)
cli.add_command(upgrade)

if __name__ == "__main__":
    cli()
