import argparse

from jrsync import core
from jrsync.management.cli import get_args


def start_from_command_line_interface():
    args: argparse.Namespace = get_args()
    core.execute(**vars(args))
