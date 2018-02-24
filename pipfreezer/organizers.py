
from .utils import get_list


def organize_packages(config, section, option, package_list, comment):
    """Organize known packages."""
    packages = []
    packages.append('\n# %s' % comment)
    for p in package_list:
        known_packages = get_list(config, section, option)
        if any(kp in p for kp in known_packages):
            packages.append(p)
            # package_list.remove(p)

    packages.sort()

    print(packages)
    return packages
