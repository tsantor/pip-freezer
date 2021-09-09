import logging
import subprocess
import glob
from collections import namedtuple

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

Package = namedtuple("Package", ["name", "version"])


def package_freeze(package_tuple):
    if package_tuple.version != "latest":
        return f"{package_tuple.name}=={package_tuple.version}"
    return package_tuple.name


class PackageData:
    """Data class so we can manipulate packages and versions easily."""

    def __init__(self, package):
        package = package.strip()
        if package.find("==") != -1:
            x = package.split("==")
            self.name = x[0].lower()
            self.version = x[1]
        else:
            self.name = package.lower()
            self.version = "latest"

    @property
    def freeze(self):
        if self.version != "latest":
            return f"{self.name}=={self.version}"
        return self.name

    def __str__(self):
        return f"PackageData(name='{self.name}', version='{self.version}')"


def get_pip_list():
    """Return a normalized lower-cased list of packages and their versions."""
    pip_freeze = subprocess.check_output(("pip", "freeze")).decode("utf8")
    package_list = [
        x.strip().split("==") for x in pip_freeze.split("\n") if x.find("==") != -1
    ]
    package_list = [Package(x[0].lower(), x[1]) for x in package_list]
    return package_list


def find_requirements_files():
    """Return a list of requirements files."""
    return glob.glob("**/requirements*.txt", recursive=True)


def open_requirements(file):
    """Return a clean list of requirements."""
    return open(file).readlines()  # [x.strip() for x in open(file).readlines()]


def get_package_tuple(package):
    """Return named of (name, version)."""
    if package.find("==") != -1:
        x = package.strip().split("==")
        return Package(x[0].lower(), x[1])
    return Package(package.lower().strip(), "latest")


def run():
    """Main program."""
    # Get pip list of installed packages
    package_list = get_pip_list()
    # print(package_list)

    # Get list of requirement files
    requirements_files = find_requirements_files()

    # for file in requirements_files:
    #     print('-' * 40)
    #     print(file)
    #     reqs = open_requirements(file)
    #     for package in reqs:
    #         print(get_package_tuple(package))

    # for line in package_list:

    # Look at each requirement and determine if it needs to be updated
    for file in requirements_files:
        lines = open_requirements(file)
        for l in lines:
            if l.startswith("#"):
                continue
            # old_package = get_package_tuple(l)
            old_package = PackageData(l)
            print(old_package.freeze)


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run()
