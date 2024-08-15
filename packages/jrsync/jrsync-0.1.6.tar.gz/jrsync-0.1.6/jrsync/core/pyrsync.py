import logging
import subprocess

from jrsync.model import Jsync
from jrsync.utils import timelib

DEFAULT_RSYNC_OPTS = "-aP"
logger = logging.getLogger("jrsync")


def can_sync_day(day: str) -> bool:
    return day == "*" or day == timelib.get_current_weekday()


def rsync(
    js: Jsync,
    src_host: str = None,
    dst_host: str = None,
    options: str = None,
    **kwargs,
) -> None:
    if not can_sync_day(js.day):
        logger.info(f"Skipping {js}")
        return

    if options is None:
        options = DEFAULT_RSYNC_OPTS

    js.override_hosts(src_host=src_host, dst_host=dst_host)
    files_to_sync = js.get_files_to_sync()
    src = js.get_src()
    dst = js.get_dst()

    for f in files_to_sync:
        command = f"rsync {options} {src}/{f} {dst}"
        if js.dst_host is not None:
            shell(f"ssh {js.dst_host} mkdir -p {js.dest_dir}", **kwargs)
        shell(command, **kwargs)


def shell(command: str, dry_run: bool = False) -> None:
    try:
        # Run the rsync command
        logger.info(f"Running: {command}")
        if dry_run:
            command = f"echo {command}"

        subprocess.run([command], check=True, text=True, shell=True)
    except Exception as e:
        logger.error(e)
