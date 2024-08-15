from datetime import datetime


def get_current_weekday(date: datetime = None) -> str:
    """
    Return the number of day using crontab convention: 0-6 with 0: Sunday, 1: Monday, ..., 6: Saturday

    Args:
        date: Input date. If None, use current date.

    Returns:
        0 if production_day is sunday, 1 if monday, ..., 6 if saturday
    """
    if date is None:
        date = datetime.now()

    weekday = date.isoweekday()  # 1: Monday, ..., 7: Sunday

    if weekday == 7:
        return "0"
    else:
        return str(weekday)
