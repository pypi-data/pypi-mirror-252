from ..core.logging import log
from ..core import config
from ..core import enums
from ..core.update import check_update
from ..core.socketUtils import disconnect

import subprocess

APP = enums.apps.Desktop


def main():
    log(f'Stamina Desktop Started! Version: {config.STAMINA_VERSION}')

    disconnect()


if __name__ == '__main__':
    main()

main()