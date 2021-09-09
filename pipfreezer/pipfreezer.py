import glob
import logging
import subprocess

# from functools import cache

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


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

    def freeze(self):
        if self.version != "latest":
            return f"{self.name}=={self.version}"
        return self.name

    def __str__(self):
        return f"PackageData(name='{self.name}', version='{self.version}')"

    def __repr__(self):
        return self.__str__()


# @cache
def get_pip_list():
    """Return a list of PackageData classes."""
    # print("subprocess")
    pip_freeze = subprocess.check_output(("pip", "freeze")).decode("utf8")
    pip_freeze = pip_freeze.split("\n")
    return [PackageData(x) for x in pip_freeze]


def get_pip_dict():
    """
    Return pip list as a dictoionary with package as key name and value
    as version.
    """
    return {p.name: p.version for p in get_pip_list()}


def find_requirements_files():
    """Return a list of requirements files."""
    return glob.glob("**/requirements*.txt", recursive=True)


def open_requirements(file):
    """Return a clean list of requirements."""
    with open(file) as fp:
        return fp.readlines()


def save_requirements(file, lines):
    "Save a list of requirements."
    with open(file, "w") as fp:
        fp.writelines(lines)


def run():
    """Main program."""
    # Get pip list of installed packages
    # package_list = get_pip_list()
    # print(package_list)
    package_dict = get_pip_dict()
    print(package_dict)

    # Get list of requirement files
    requirements_files = find_requirements_files()

    # Look at each requirement file line by line and determine if a package
    # needs to be updated
    for file in requirements_files:
        lines = open_requirements(file)
        replaced_content = ""
        for line in lines:
            # simply re-add comments or empty lines
            if line.startswith("#") or line.startswith("\n"):
                replaced_content += line
                continue

            package = PackageData(line)
            version_mismatch = package.version != package_dict[package.name]
            if package.name in package_dict and version_mismatch:
                package.version = package_dict[package.name]
                print(
                    f"Updated {package.name} from {package.version} to {package_dict[package.name]}"
                )
                replaced_content += package.freeze() + "\n"
            save_requirements(file, replaced_content)


if __name__ == "__main__":
    run()
