from colorama import Fore
from colorama import Style


def print_message(color: str, message: str) -> None:
    """Print a message with color."""
    print(f"{color}{message}{Fore.RESET}")  # noqa: T201


def print_updated_packages(packages: list) -> None:
    """Print a list of updated packages."""
    print_message(Fore.GREEN, "The following packages have updated pinned versions:")
    print_message(Style.DIM, "\n".join(packages))


def print_not_installed_packages(packages: list) -> None:
    """Print a list of packages that are not installed."""
    print_message(
        Fore.YELLOW,
        "\nThe following packages are referenced in requirements, "
        "but are not installed:",
    )
    print_message(Style.DIM, "\n".join(packages))
