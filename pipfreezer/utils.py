

def get_list(config, section, option):
    """Get list from config with multi-line value."""
    value = config.get(section, option)
    return list(filter(None, (x.strip().lower() for x in value.splitlines())))
