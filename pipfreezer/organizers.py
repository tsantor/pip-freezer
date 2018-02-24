
from .utils import get_list


def organize_packages(comment, known_packages, package_list):
    """Organize known packages."""
    packages = []
    packages.append('\n# %s' % comment)
    to_remove = []
    # known_packages.reverse()
    # print('package_list:', package_list)
    # print(known_packages)
    for p in package_list:
        if any(kp in p for kp in known_packages):
            packages.append(p)
            to_remove.append(p)

    # Remove packages from package_list
    # print('To remove:', to_remove)
    for p in to_remove:
        # print(p)
        if p in package_list:
            # print('Remove:', p)
            package_list.remove(p)

    packages.sort()

    if len(packages) > 1:
        # print(packages)
        return packages
    return []
