import re

ADDRESS = re.compile(".+@.+")


def is_valid_address(s: str) -> bool:
    return s is not None and ADDRESS.fullmatch(s) is not None
