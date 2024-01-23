import os
import json
from ..core import utils
from ..core.logging import log


def create_step(step, proj_code):
    config = utils.get_config()

    # CHECKING
    # If project doesn't exist, raise error
    if not proj_code in config['project_list'].keys():
        raise ValueError(f'Project <{proj_code}> does not exist.')
    # if there is no project list in the config file for this project, create it
    if not 'step_list' in config['project_list'][proj_code]:
        config['project_list'][proj_code]['step_list'] = []



    # If step already exist in project, raise error
    if step in config['project_list'][proj_code]['step_list']:
        raise ValueError(f'Step <{step}> already exists for this project.')

    # check step name conventions

    # SETTING
    # Add step
    config['project_list'][proj_code]['step_list'].append(step)
    utils.put_config(config)


def remove_step(step, proj_code):
    """
    Will not remove all the directories for each entities, in case there are some stuff into it.
    :param step: step to remove
    :param project: project to remove step from.
    :return: Nothing
    """
    config = utils.get_config()

    # CHECKING
    # does project exists?
    if not proj_code in config['project_list'].keys():
        raise ValueError(f'Project <{proj_code}> does not exist.')

    # Is there any step list?
    if not 'step_list' in config['project_list'][proj_code]:
        config['project_list'][proj_code]['step_list'] = []
        utils.put_config(config)
        raise ValueError('There is not any step for this project.')

    # Does the step exist?
    if not step in config['project_list'][proj_code]['step_list']:
        raise ValueError(f'Step <{step}> does not exist for this project.')

    # DELETING
    # Delete step
    i = config['project_list'][proj_code]['step_list'].index(step)
    del config['project_list'][proj_code]['step_list'][i]
    utils.put_config(config)
