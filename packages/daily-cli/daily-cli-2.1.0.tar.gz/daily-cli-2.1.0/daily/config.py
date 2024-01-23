""" Functions related to daily's config

Add any new entries to daily.ini by adding the entry to the default
string in this file.
"""

import configparser
import os
from pathlib import Path


home = Path.home()

user_confdir = f'{home}/.config/daily'
user_conf = f'{user_confdir}/daily.ini'


default = f"""\
[default]

# Path to journal
journal = {home}/.local/share/daily

# Store entries as md or rst
entry_format = md

# Create new entries by copying a previous entry referenced by a date.
# Plain english date strings are accepted; like "last week".
#
# If the entry doesn't exist, then daily will walk backwards up to a year
# until it finds one. If that doesn't happen then a simple blank entry will
# be created.
copy_previous =
"""


def get_defaults():
    """ Default values for items that should be in a config file.

    These values will be overuled by existing config entries. Useful in
    the event a config file is missing an entry.

    Returns:
        A dictionary that contains all expected entries for a
        configuration file.
    """
    c = configparser.ConfigParser()
    c.read_string(default)
    return dict(c['default'])

def do_first_time_setup():
    """ Create default ini in user conf path.
    """
    try:
        os.makedirs(user_confdir)
    except FileExistsError:
        pass

    with open(user_conf, 'w') as f:
        f.write(default)

    os.makedirs(f'{home}/.local/share/daily', exist_ok=True)


def add_config_args(args, config=None):
    """ Add params from a config file to an ArgumentParser.

    Parameters are only copied if not already set in the
    ArgumentParser.

    Args:
        args: ArgumentParser instance.
        config: Path to config file.

    Returns:
        namedtuple containing config parameters overridden by command
        line arguments.

    Raises:
        FileNotFoundError: Provided config file doesn't exist.
        KeyError: Configuration file has no default section (or no sections).
    """
    config = user_conf if not config else config

    if not os.path.exists(config):
        raise FileNotFoundError('Config {} does not exist.'.format(config))

    cp = configparser.ConfigParser()

    try:
        cp.read(config)
    except Exception as e:
        raise KeyError('Config "{}" is invalid. {}.'.format(config, e))

    if 'default' not in cp:
        raise KeyError('Config {} has no "default" section.'.format(config))

    d = get_defaults()
    d.update(cp['default'])

    # copy vals into args if not already in args.
    for key, val in d.items():
        try:
            if not getattr(args, key):
                setattr(args, key, val)
        except AttributeError:
            setattr(args, key, val)

    return args
