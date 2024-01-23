from enum import Enum
from ..core import project
from ..core import utils
from ..core import constants
from ..core import step
import os
import shutil


class entityTypes(Enum):
    SHOT = 0
    ASSET = 1


def get_entity_path(entity_type, entity_code, proj_code):
    proj_path = project.get_remote_path(proj_code)
    config = utils.get_config()
    if entity_type == entityTypes.SHOT:
        entity_folder = 'shots'
    elif entity_type == entityTypes.ASSET:
        entity_folder = 'assets'

    local_path = utils.fix_path(os.path.join(config['project_list'][proj_code]['local_path'], entity_folder))
    remote_path = utils.fix_path(os.path.join(config['project_list'][proj_code]['remote_path'], entity_folder))
    return {'local_path': local_path, 'remote_path': remote_path}


def entity_exists(entity_type, entity_code, proj_code):
    """
    Checks if the entity exists
    """
    entity_list = None

    if entity_type == entityTypes.SHOT:
        entity_list = 'shot_list'
        entity_folder = 'shots'
    elif entity_type == entityTypes.ASSET:
        entity_list = 'asset_list'
        entity_folder = 'assets'

    list = os.listdir(get_entity_path(entity_type, entity_code, proj_code)['remote_path'])
    print(list)
    if entity_code in list:
        return entity_code
    else:
        return None


def create_entity(entity_type, entity_code, proj_code):
    config = utils.get_config()

    # CHECKING
    # entity_type is of good type
    if not type(entity_type) == entityTypes:
        raise TypeError('Entity is of wrong type.')

    # Does the project exist?
    if not project.get_proj_code(proj_code):
        raise ValueError('No project exists with this code.')

    # Does the entity exist already?
    if entity_exists(entity_type, entity_code, proj_code):
        raise ValueError('An entity already of this type exist with that code.')

    # CREATING
    # Creating entity root directory
    if entity_type == entityTypes.SHOT:
        entity_folder = 'shots'
    elif entity_type == entityTypes.ASSET:
        entity_folder = 'assets'
    entity_local_path = utils.fix_path(os.path.join(config['project_list'][proj_code]['local_path'], entity_folder, entity_code))
    entity_remote_path = utils.fix_path(os.path.join(config['project_list'][proj_code]['remote_path'], entity_folder, entity_code))
    os.makedirs(entity_local_path)
    os.makedirs(entity_remote_path)

    # Creating step directories
    steps = step.steps(proj_code)
    for _step in steps:
        local = utils.fix_path(os.path.join(entity_local_path, _step))
        remote = utils.fix_path(os.path.join(entity_remote_path, _step))

        os.makedirs(local)
        os.makedirs(remote)


def remove_entity(entity_type, entity_code, proj_code):
    config = utils.get_config()
    if entity_type == entityTypes.SHOT:
        entity_folder = 'shots'
    elif entity_type == entityTypes.ASSET:
        entity_folder = 'assets'

    # CHECKING
    # Does the entity exist?
    check = entity_exists(entity_type, entity_code, proj_code)
    print(check, entity_type, entity_code, proj_code)
    if not check:
        raise ValueError('Entity does not exist.')

    # REMOVING
    entity_local_path = utils.fix_path(os.path.join(config['project_list'][proj_code]['local_path'], entity_folder, entity_code))
    entity_remote_path = utils.fix_path(os.path.join(config['project_list'][proj_code]['remote_path'], entity_folder, entity_code))
    shutil.rmtree(entity_local_path)
    shutil.rmtree(entity_remote_path)