import os
import json
from ..core import utils
from ..core.logging import log


def get_proj_code(code):
    config = utils.get_config()

    # Does project exists in config file?
    if code in config['project_list'].keys():
        return code
    else:
        return None


def get_local_path(code):
    config = utils.get_config()
    local_path = config['project_list'][code]['local_path']
    if os.access(local_path, os.F_OK):
        return local_path
    else:
        return None


def get_remote_path(code):
    config = utils.get_config()
    remote_path = config['project_list'][code]['remote_path']

    if os.access(remote_path, os.F_OK):
        return remote_path
    else:
        return None


def create_project(code, local_path, remote_path):
    """

    """
    # Does the project exist?
    if get_proj_code(code):
        raise ValueError('Project already exists in config file')
    elif get_local_path(code):
        raise FileExistsError('local_path already exists.')
    elif get_remote_path(code):
        raise FileExistsError('remote_path already exists.')

    # Create local & remote folders
    local_path = utils.fix_path(os.path.join(local_path, code))
    remote_path = utils.fix_path(os.path.join(remote_path, code))

    config = utils.get_config()



    # Write project to config file
    proj_dict = {
        'local_path': local_path,
        'remote_path': remote_path
    }
    config['project_list'][code] = proj_dict

    # Create folders
    try:
        os.makedirs(local_path)
        os.makedirs(remote_path)

        os.makedirs(utils.fix_path(os.path.join(remote_path, 'assets')))
        os.makedirs(utils.fix_path(os.path.join(remote_path, 'shots')))
    except Exception as e:
        raise e

    utils.put_config(config)
    log(f'Successfully Created project {code}')


def add_project(code, local_path, remote_path):
    local_path = utils.fix_path(os.path.join(local_path, code))
    remote_path = utils.fix_path(remote_path)

    config = utils.get_config()

    # is there already a project with the code in config file?
    if code in config['project_list'].keys():
        raise ValueError('A project with this code already exists in the config file')

    # Is local path empty? If not, raise error
    if os.access(local_path, os.F_OK):
        raise FileExistsError('local_path already exists.')

    # Does remote_path exists? if not, raise error
    elif not os.access(remote_path, os.F_OK):
        print(not os.access(remote_path, os.F_OK))
        print(remote_path)
        raise FileExistsError(r"remote_path is not reachable. Verify you're connected to the server.")

    # Create local_path
    try:
        os.makedirs(local_path)
    except FileExistsError:
        raise FileExistsError(f'The destination folder already contains a project called {code}. Please select an empty directory.')

    # Add project to config if it's not already in it
    proj_dict = {
        'local_path': local_path,
        'remote_path': remote_path
    }
    config['project_list'][code] = proj_dict
    utils.put_config(config)
    log(f'Successfully added project {code}')


def set_project():
    pass


def remove_project(code, remove_local=False, remove_remote=False):
    # Do I remove the Local Files?
    config = utils.get_config()
    if not code in config['project_list'].keys():
        raise FileExistsError(f'No project exists in config file with the code {code}')

    local_path = config['project_list'][code]['local_path']
    remote_path = config['project_list'][code]['remote_path']

    if remove_local:
        os.rmdir(local_path)
    if remove_remote:
        os.rmdir(remote_path)

    del config['project_list'][code]

    utils.put_config(config)
    log(f'Successfully removed project {code}.')

