import os
import json
from ..core import constants

def fix_path(old_path, new_sep='/'):
    """
    Will make sure all path have the same / or \.
    """
    _path = old_path.replace('\\', '/')
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('//', '/')

    if _path.endswith('/'):
        _path = _path[:-1]

    _path = _path.replace('/', new_sep)

    new_path = _path
    return new_path


def get_config():
    with open(os.path.join(constants.STM_CONFIG_PATH, 'config.json'), 'r+') as f:
        config_str = f.read()
        config = json.loads(config_str)
        # print(config)
        return config


def put_config(config):
    with open(os.path.join(constants.STM_CONFIG_PATH, 'config.json'), 'w+') as f:
        json.dump(config, f, indent=4)
        # f.write(config)
        # print(config)