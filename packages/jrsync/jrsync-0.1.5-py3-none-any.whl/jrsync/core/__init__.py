import logging

import jrsync
import jrsync.conf as settings
from jrsync.core import main
from jrsync.core import pid_control

logger = logging.getLogger("jrsync")


def execute(**kwargs):
    jrsync.setup()

    kwargs.pop("get_version")
    force_mode = kwargs.pop("force", settings.DEFAULT_FORCE_MODE)

    config_name = kwargs["config"].stem
    if not force_mode and not pid_control.get_exec_permission(config_name):
        logger.warning("Another instance in execution, exiting")
        exit(0)

    main.execute(**kwargs)
