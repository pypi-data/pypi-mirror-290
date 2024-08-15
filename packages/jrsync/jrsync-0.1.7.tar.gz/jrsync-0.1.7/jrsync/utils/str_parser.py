#!/usr/bin/env python
import re
import subprocess
from datetime import timedelta, datetime

import jrsync.conf as settings

RE_DATE = re.compile(settings.DATE_PLACEHOLDER_REGEX)


def replace_dates(input_str, ref_date: datetime) -> str:
    """
    Find and substitute all {{DATE-i}} pattern in the string with the correct date.
    This function will ignore all the system variables.
    """
    resolved_str = input_str.replace(" ", "")
    occurrences = RE_DATE.findall(resolved_str)
    if len(occurrences) == 0:
        return input_str

    # replace one by one each date placeholder
    for date_plh in occurrences:
        resolved_date = resolve_date_plh(date_plh, ref_date)
        resolved_str = resolved_str.replace(date_plh, resolved_date)

    return resolved_str


def resolve_date_plh(date_template: str, ref_date: datetime) -> str:
    """
    Replace date template with the correct data in the format YYYYMMDD
    :param ref_date: date to se as reference to substitute to date_template
    :param date_template: String with the following template:
        {{DATE}} -> replaced with the bulletin date
        {{DATE [+-] i}} -> replaced with the bulletin date decreased of i times
    :return:
    """
    if date_template == settings.DATE_PLACEHOLDER:
        date_to_return = ref_date
    else:
        sign = "+" if "+" in date_template else "-"
        days_to_add = date_template.split(sign)[-1].strip("}")
        date_to_return = ref_date + timedelta(days=int(sign + days_to_add))

    return date_to_return.strftime(settings.DATE_FMT)


def resolve_str(
        input_str: str, ref_date: datetime
) -> str:
    final_str = replace_dates(input_str, ref_date)

    if "$" in final_str:
        final_str = evaluate_str_with_bash(final_str)

    return final_str


def evaluate_str_with_bash(input_str: str) -> str:
    """
    Retrieves the evaluated value of a Bash-style variable expression.

    Args:
        input_str (str): Input string to be evaluated and resolved.
            e.g., 'foo${var}' or 'foo${var:-"default"}' or $((expr)).
    Returns:
        str: The input str evaluated by the Bash shell.
    Raises:
        ValueError: If an unbound variable is encountered.

    Example:
        >>> evaluate_str_with_bash('foo${var}foo')
        'foobarfoo'
    """
    try:
        result = subprocess.run(
            f"set -o nounset; echo {input_str}",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return (
            result.stdout.strip()
        )  # Get the stdout output and strip any extra whitespace
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Undefined variable: '{input_str}'") from e
