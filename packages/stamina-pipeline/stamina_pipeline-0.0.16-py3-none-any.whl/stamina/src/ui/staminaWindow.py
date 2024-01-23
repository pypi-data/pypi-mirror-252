from ..core.logging import log
from ..core import config
from ..core import enums
from ..core.socketUtils import disconnect
from ..core import utils

import subprocess, userpaths, os, json

APP = enums.apps.Desktop
STM_CONFIG_PATH = documents = os.path.join(userpaths.get_my_documents(), '__stamina__')


def get_config():
    with open(os.path.join(STM_CONFIG_PATH, 'config.json'), 'r+') as f:
        config_str = f.read()
        config = json.loads(config_str)
        return config


def update_plugins():
    # config = get_config()
    # # Maya
    # mayapy_path = utils.fix_path(config['paths']['maya_path'])
    # print(mayapy_path)
    # subprocess.Popen(f'cd {mayapy_path}& mayapy.exe -m pip install --no-cache-dir stamina_pipeline --upgrade --user', shell=True)
    #
    #
    # # Houdini
    # hython_path = utils.fix_path(os.path.join(config['paths']['houdini_path'], 'hython.exe'))
    # print(hython_path)
    # # os.system(f'{hython_path} -m pip install --no-cache-dir stamina_pipeline --upgrade --user')


    return


def main():
    log(f'Stamina Desktop Started! Version: {config.STAMINA_VERSION}')

    update_plugins()

    disconnect()


if __name__ == '__main__':
    main()

main()