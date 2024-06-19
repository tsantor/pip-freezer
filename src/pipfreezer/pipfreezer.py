import json
import logging
import subprocess
from pathlib import Path

from . import PackageData

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Requirements Files
# -----------------------------------------------------------------------------


def find_requirements_files() -> list[Path]:
    """Return a list of requirements files recursively."""
    return list(Path().rglob("requirements/*.txt")) + list(
        Path().rglob("requirements*.txt")
    )


def open_requirements(file) -> list[str]:
    """Return a clean list of requirements."""
    with Path(file).open() as fp:
        return fp.readlines()


def save_requirements(file, lines) -> None:
    "Save a list of requirements."
    with Path(file).open("w") as fp:
        fp.writelines(lines)


def update_requirements_file(
    file: str, package_dict: dict
) -> tuple[list[str], list[str]]:
    """Open and update the requirements file."""
    replaced_content = ""
    updated = []
    not_installed = []

    lines = open_requirements(file)
    # Go line by line and determine if a package needs to be updated
    for line in lines:
        # Simply re-add comments or empty lines
        if bool(line.startswith(("#", "\n", "-r"))):
            replaced_content += line
            continue

        package = PackageData(line)
        if package.name in package_dict:
            pkg_version = package_dict[package.name]
            if package.version != pkg_version:
                updated.append(f"{package.name} {package.version} => {pkg_version}")
                package.version = pkg_version
            replaced_content += package.freeze() + "\n"
        else:
            replaced_content += line
            not_installed.append(package.name)

    # Save the updated requirements file after all lines have been processed
    save_requirements(file, replaced_content)
    return updated, not_installed


# -----------------------------------------------------------------------------
# Call Subprocesses
# -----------------------------------------------------------------------------


def get_pip_list_as_json() -> str:
    """Return a JSON string of installed packages."""
    cmd = ["python3", "-m", "pip", "list", "--format", "json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)  # noqa: S603
    return proc.stdout.strip()


def get_pip_list_outdated_as_json() -> str:
    """Return a JSON string of outdated packages."""
    cmd = ["python3", "-m", "pip", "list", "--outdated", "--format", "json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)  # noqa: S603
    return proc.stdout.strip()


def upgrade_outdated_packages(to_install: str) -> str:  # pragma: no cover
    """Upgrade outdated packages."""
    cmd = ["python3", "-m", "pip", "install", "--upgrade"] + to_install
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)  # noqa: S603
    return proc.stdout.strip()


# -----------------------------------------------------------------------------


def get_package_data_from_json_output(json_str: str) -> list[PackageData]:
    """Return a list of PackageData classes based on pip list json output."""
    packages = json.loads(json_str)
    return [PackageData(f"{pkg['name']}=={pkg['version']}") for pkg in packages]


def get_package_data_from_requirements() -> list[PackageData]:
    """Return a list of PackageData classes."""
    requirements = [
        line.strip()
        for f in find_requirements_files()
        for line in open_requirements(f)
        if not bool(line.startswith(("#", "\n", "-r")))
    ]
    return [PackageData(pkg) for pkg in requirements]


def get_pip_dict(json_str: str) -> dict[str, str]:
    """Return pip list as a dictionary with package as key name and value
    as version."""
    return {p.name: p.version for p in get_package_data_from_json_output(json_str)}
