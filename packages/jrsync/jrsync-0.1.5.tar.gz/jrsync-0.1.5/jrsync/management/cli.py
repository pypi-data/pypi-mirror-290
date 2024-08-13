import argparse
import datetime
import importlib.metadata
import sys
from pathlib import Path

from jrsync import core


class DataParser(argparse.Action):
    def __call__(self, parser, namespace, values, option_strings=None):
        setattr(namespace, self.dest, datetime.datetime.strptime(values, "%Y%m%d"))


def get_args(raw_args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Jrsync CLI")

    parser.add_argument(
        "config", type=Path, help="Json file containing sync information"
    )
    parser.add_argument(
        "date_to_sync", action=DataParser, help="Date in the format YYYYMMDD"
    )
    parser.add_argument(
        "--src-host",
        dest="src_host",
        default=None,
        type=str,
        help="Source address. Example: user@remote",
    )
    parser.add_argument(
        "--dst-host",
        dest="dst_host",
        default=None,
        type=str,
        help="Dest address. Example: user@remote",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow to run multiple instance in the same moment",
    )
    parser.add_argument(
        "-o",
        "--options",
        type=str,
        help="Rsync options. use -o|--options= to avoid conflicts with python args",
    )
    parser.add_argument(
        "-d"
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Enable dry run mode",
    )
    parser.add_argument(
        "-V",
        "--version",
        dest="get_version",
        default=False,
        action="store_true",
        help="Print version and exit",
    )
    if "-V" in sys.argv or "--version" in sys.argv:
        print(importlib.metadata.version("jrsync"))
        sys.exit(0)
    return parser.parse_args(raw_args)


if __name__ == "__main__":
    args: argparse.Namespace = get_args()
    core.execute(**vars(args))
