from ..core import config
from ..core.logging import log
from ..core.socketUtils import send
from ..core.enums import messageTypes

import requests, subprocess, sys, importlib, json


def check_update():
    if config.DEV:
        pass
    else:
        log('Checking for update...')
        kwargs = {'client_current_version': config.STAMINA_VERSION}
        update_available = int(send(msg_type=messageTypes.check_for_update, msg_text=kwargs))
        # update_available = True if update_available == ''
        if update_available:
            log('Update available, starting update.')
            return 1
        else:
            log('Stamina is up to date.')
            return 0
