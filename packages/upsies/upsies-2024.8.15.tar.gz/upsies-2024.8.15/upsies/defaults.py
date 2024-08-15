import functools

from . import constants, trackers, utils

defaults = {
    'config': {
        'main': {
            'cache_directory': utils.configfiles.config_value(
                value=constants.DEFAULT_CACHE_DIRECTORY,
                description='Where to store generated files.',
            ),
            'max_cache_size': utils.configfiles.config_value(
                value=utils.types.Bytes.from_string('100 MB'),
                description=(
                    'Maximum size of cache directory. '
                    'Units like "kB" and "MiB" are interpreted.'
                ),
            ),
        },
        'torrent-create': {
            'reuse_torrent_paths': utils.configfiles.config_value(
                value=[],
                description=(
                    'List of directories to search for a *.torrent file '
                    'to get piece hashes from instead of generating the '
                    'pieces hashes from file contents.'
                ),
            ),
        },
        'screenshots': {
            'optimize': utils.configfiles.config_value(
                value=utils.types.Choice('default', options=utils.image.optimization_levels),
                description='Whether to optimize screenshot file sizes with oxipng.',
            ),
        },
        'id': {
            'show_poster': utils.configfiles.config_value(
                value=utils.types.Bool('no'),
                description='Whether to display a poster for easier identification.',
            ),
        },
    },

    'trackers': {
        tracker.name: tracker.TrackerConfig()
        for tracker in trackers.trackers()
    },

    'imghosts': {
        imghost.name: imghost.default_config
        for imghost in utils.imghosts.imghosts()
    },

    'clients': {
        name: utils.btclient.client_defaults(name)
        for name in utils.btclient.client_names()
    },
}
"""Defaults for configuration options"""


@functools.lru_cache(maxsize=None)
def option_paths():
    """Tuple of configuration option paths (`<section>.<subsection>.<option>`)"""
    return utils.configfiles.ConfigFiles(defaults).paths


def option_type(option_path):
    filename, section, option = option_path.split('.', maxsplit=2)
    return type(defaults[filename][section][option])
