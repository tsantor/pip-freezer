
# for each_section in conf.sections():
#     for (each_key, each_val) in conf.items(each_section):
#         print each_key
#         print each_val

def get_list(config, section, option):
    """Get list from config with multi-line value."""
    value = config.get(section, option)
    return list(filter(None, (x.strip().lower() for x in value.splitlines())))
