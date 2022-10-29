import calendar
from datetime import datetime
import moon_api
import json
import asyncio


def _get_current_dmy():
    """Returns current day and month."""
    day_current = datetime.today().strftime("%d")
    month_current = datetime.today().strftime("%m")
    year_current = datetime.today().strftime("%Y")

    dm = [int(day_current), int(month_current), int(year_current)]
    return dm


def days_to_fullmoon():
    """Returns how many days until fullmoon."""
    # Get current day, month, year in a list.
    dmy = _get_current_dmy()

    # Get fullmoon day, be it next month or this.
    fullmoon_day = moon_api.get_fullmoon()

    if not moon_api.is_fullmoon_over(fullmoon_day):
        # If fullmoon is this month now.
        days = dmy[0] - int(fullmoon_day)
    else:
        # If fullmoon is next month.

        # Returns how many days this current month has.
        month_days = calendar.monthrange(dmy[2], dmy[1])

        temp = int(month_days[1]) - dmy[0]
        days = temp + int(fullmoon_day)

    return int(days)


async def update_days():
    """Updates reminder file to represent days."""
    days_to_fullmoon_int = days_to_fullmoon()
    days_to_fullmoon_int = int(days_to_fullmoon_int)
    try:
        with open("files/reminder.json", "r") as f:
            days_file = json.load(f)
            reminded = days_file["reminded"]
        if days_file["days"] > days_to_fullmoon_int:
            with open("files/reminder.json", "w") as f:
                info = {"days": days_to_fullmoon_int, "reminded": reminded}
                json.dump(info, f)
                return days_to_fullmoon_int
        else:
            with open("files/reminder.json", "w") as f:
                info = {"days": days_file["days"], "reminded": reminded}
                json.dump(info, f)
                return int(days_file["days"])
    except FileNotFoundError:
        print("Debug Log: Reminder File not found, creating one...")
        with open("files/reminder.json", "w") as f:
            info = {"days": days_to_fullmoon_int, "reminded": False}
            json.dump(info, f)
            print(f"\tInfo: Created file with reminded = False and days = {days_to_fullmoon_int}")
            return days_to_fullmoon_int


def is_reminded():
    """Checks if user has been reminded, if not return false."""

    with open("files/reminder.json", "r") as f:
        days_file = json.load(f)
        if days_file["reminded"]:
            return True
        else:
            return False


# Is called to update the reminded tag. (Parameter to set either to True or False)
def was_reminded(reminded):
    """Writes reminded into file if user was reminded."""
    with open("files/reminder.json", "r") as f:
        days = json.load(f)

    with open("files/reminder.json", "w") as f:
        info = {"days": int(days["days"]), "reminded": reminded}
        json.dump(info, f)


# Requires that reminder.json is up-to-date!
def need_remind():
    """Checks if reminder is necessary."""
    days = days_to_fullmoon()

    with open("files/reminder.json", "r") as f:
        days_i = json.load(f)

    if days <= 14 and not days_i["reminded"]:
        return True
    else:
        return False


# Test for functions
if __name__ == "__main__":
    # print(_get_current_dmy())
    # print(update_days())
    # print(need_remind())
    # print(is_reminded())
    print(is_reminded())
