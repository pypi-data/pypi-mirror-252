from ..core.logging import log
from ..core import enums
from ..core.update import check_update
from ..core.socketUtils import disconnect

import subprocess

APP = enums.apps.Desktop


def main():
    log('Stamina Desktop Started!')

    if check_update():
        # subprocess.run(['python -m pip install stamina_pipeline'])
        subprocess.run(r'update.bat')
        disconnect()
        return


    disconnect()

if __name__ == '__main__':
    main()

main()

