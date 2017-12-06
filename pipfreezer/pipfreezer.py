import logging
import subprocess
import os

from . import config, args

# -----------------------------------------------------------------------------


def exec_cmd(cmd):
    """Executes a command and returns its output."""
    logger = logging.getLogger(__name__)
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                       shell=True)
    except subprocess.CalledProcessError:
        logger.error('Command failed: %s', cmd)


def get_list(config, section, option):
    """Get list from config with multi-line value."""
    value = config.get(section, option)
    return list(filter(None, (x.strip().lower() for x in value.splitlines())))


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

    itemlist.sort()

    # Write new file
    with open(filename, 'w') as f:
        fname = os.path.basename(filename)
        if 'local' in fname:
            f.write('# Local development dependencies go here\n-r base.txt\n\n')
        if 'production' in fname:
            f.write('# Pro-tip: Try not to put anything here. Avoid dependencies in production that aren\'t in development.\n-r base.txt\n\n')
        if 'test' in fname:
            f.write('# Test dependencies go here.\n-r base.txt\n\n')
        if 'unknown' in fname:
            f.write('# Unknown dependencies go here. Probably dependencies of top level packages.\n-r base.txt\n\n')
        for item in itemlist:
            f.write('%s\n' % item)


def package_version(package_info):
    """Reassemble package info."""
    return '=='.join(package_info)


def run():
    """Main program."""
    logger = logging.getLogger(__name__)

    # Determine pip path
    if config.has_option('default', 'pip_path'):
        pip_path = config.get('default', 'pip_path')
    else:
        pip_path = 'pip'

    # Get known packages
    base_packages = get_list(config, 'base', 'packages')
    local_packages = get_list(config, 'local', 'packages')
    prod_packages = get_list(config, 'production', 'packages')
    test_packages = get_list(config, 'test', 'packages')

    base_list = []
    local_list = []
    prod_list = []
    test_list = []
    unknown_list = []

    # Get package list
    package_list = get_package_list()
    for line in package_list:
        # print(line)
        pack_ver = package_version(line)
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
            logger.debug('%s is a unknown package (probably a dependency of a top level package)' % line[0])
            unknown_list.append(pack_ver)

    if base_list:
        list_to_file(base_list, 'requirements/base.txt')

    if local_list:
        list_to_file(local_list, 'requirements/local.txt')

    if prod_list:
        list_to_file(prod_list, 'requirements/production.txt')

    if test_list:
        list_to_file(test_list, 'requirements/test.txt')

    if unknown_list and args.unknown:
        list_to_file(unknown_list, 'requirements/unknown.txt')

    # Remove requirements.txt
    if os.path.exists('requirements.txt'):
        os.remove('requirements.txt')

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run()
