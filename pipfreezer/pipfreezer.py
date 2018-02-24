import logging
import subprocess
import os

from . import config, args
from .organizers import organize_packages
from .utils import get_list

# -----------------------------------------------------------------------------


# def get_list(config, section, option):
#     """Get list from config with multi-line value."""
#     value = config.get(section, option)
#     return list(filter(None, (x.strip().lower() for x in value.splitlines())))


def get_package_list():
    """Return a normalized lower-cased list of packages and their versions."""
    pip_freeze = subprocess.check_output(('pip', 'freeze')).decode('utf8')
    package_list = [x.strip().split('==') for x in pip_freeze.split('\n') if x.find('==') != -1]
    package_list = [(x[0].lower(), x[1]) for x in package_list]
    # package_map = {x[0].lower(): x[1] for x in package_list}
    return package_list


def list_to_file(itemlist, filename):
    """Save requirements to file."""
    # Create dir if needed
    dir_path = os.path.dirname(filename)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    # Delete existing file
    if os.path.exists(filename):
        os.remove(filename)

    # itemlist.sort()

    # Write new file
    with open(filename, 'w') as f:
        fname = os.path.basename(filename)
        if 'local' in fname:
            f.write('# Local development dependencies go here\n-r base.txt\n\n')
        if 'production' in fname:
            f.write('# Pro-tip: Try not to put anything here. Avoid dependencies in production that aren\'t in development.\n-r base.txt\n\n')
        if 'test' in fname:
            f.write('# Test dependencies go here.\n-r base.txt\n\n')
        if 'subdependencies' in fname:
            f.write('# Sub-dependencies (i.e. dependencies of top level dependencies).\n-r base.txt\n\n')
        for item in itemlist:
            f.write('%s\n' % item)


def run():
    """Main program."""
    logger = logging.getLogger(__name__)

    # Get known packages
    base_packages = get_list(config, 'base', 'packages')
    local_packages = get_list(config, 'local', 'packages')
    prod_packages = get_list(config, 'production', 'packages')
    test_packages = get_list(config, 'test', 'packages')

    base_list = []
    local_list = []
    prod_list = []
    test_list = []
    sub_list = []

    # Get package list
    package_list = get_package_list()
    for line in package_list:
        # print(line)
        pack_ver = '=='.join(line)
        is_added = False

        # Place packages into their corresponding files
        if line[0] in base_packages:
            base_list.append(pack_ver)
            is_added = True
        if line[0] in local_packages:
            local_list.append(pack_ver)
            is_added = True
        if line[0] in prod_packages:
            prod_list.append(pack_ver)
            is_added = True
        if line[0] in test_packages:
            test_list.append(pack_ver)
            is_added = True

        # We don't know where these go?
        if not is_added:
            logger.debug('%s is a unknown package (probably a sub-dependency of a top level package)' % line[0])
            sub_list.append(pack_ver)


    # TODO: Futher organize
    drf_packages = organize_packages(config, 'djangorestframework', 'packages', base_list, "Django Rest Framework")

    # Create organized requirements files
    if base_list:
        list_to_file(base_list + drf_packages, 'requirements/base.txt')

    if local_list:
        list_to_file(local_list, 'requirements/local.txt')

    if prod_list:
        list_to_file(prod_list, 'requirements/production.txt')

    if test_list:
        list_to_file(test_list, 'requirements/test.txt')

    if sub_list and args.sub:
        list_to_file(sub_list, 'requirements/subdependencies.txt')

    # Remove requirements.txt
    if os.path.exists('requirements.txt'):
        os.remove('requirements.txt')

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run()
