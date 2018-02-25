

def get_list(config, section, option):
    """Get list from config with multi-line value."""
    value = config.get(section, option)
    return list(filter(None, (x.strip().lower() for x in value.splitlines())))


def item_to_label(key):
    """Take a section item and make a human readable label."""
    parts = key.split('_')
    parts = [p.title() for p in parts]
    return ' '.join(parts)


def get_package_labels(config):
    for section in config.sections():
        print('-' * 40)
        print(section)
        print('-' * 40)
        for key, val in config.items(section):
            print(item_to_label(key))
            # print(key)
            # print(val)


def get_packages(config):
    """Return a tuple of flat package lists for all sections."""
    requirements = []
    for section in config.sections():
        packages = []
        for key, val in config.items(section):
            lines = filter(None, (x.strip().lower() for x in val.splitlines()))
            lines.pop(0)
            packages += list(lines)
        packages.sort()
        requirements.append(packages)

    return tuple(requirements)
