"""Custom python file which can get info of the moon"""

# Default Imports
from datetime import datetime
import re  # Regex
import urllib.request
import calendar

import requests


def get_current_moonphase():
    """Gets the current moon phase"""
    # Gets current date and creates fitting url
    today = datetime.today().strftime("%m/%d/%Y")
    url = "https://www.moongiant.com/phase/" + today + "/"

    # Loads Page
    r = requests.get(url)
    # print(f"Debug Log: Status Code of Moon API: {r.status_code}.\n")

    page_text = r.text

    # Regex finding the moon phase information on page.
    moon_phase = re.findall("Phase: <span>(.*)</span>", page_text)

    # Returns moon phase
    moon = f"{moon_phase[0]}"
    return moon


def get_c_mphase_image():
    """Get an image of the current moon phase."""
    # Gets current date and creates fitting url
    today = datetime.today().strftime("%m/%d/%Y")
    url = "https://www.moongiant.com/phase/" + today + "/"

    # Gets Page and loads it as text
    r = requests.get(url)
    # print(f"Debug Log: Status Code of Moon API: {r.status_code}.\n")

    page_text = r.text

    # Finding the image of today's moon and creating an url to that image
    moon_image_url = re.findall('<div id="todayMoonContainer"><img src="(.*)" width="164"', page_text)
    url_image = "https://www.moongiant.com" + moon_image_url[0]

    # Retrieving image from url and saving it.
    urllib.request.urlretrieve(url_image, "files/images/moon_phase.jpg")

    # Old way to transfer image, wasn't working with discord.py
    # img = Image.open(BytesIO(r.content))

    # Returns path to image
    return "files/images/moon_phase.jpg"


def get_fullmoon(month=None):
    """Returns date for the full moon."""
    # Page with all full moons this year.
    url = "https://www.moongiant.com/fullmoons/"

    # Request site as text
    r = requests.get(url)
    page_text = r.text

    if month == None:
        # Get Months and so on as texts
        month_text = datetime.today().strftime("%B")
        # month_text_short = datetime.today().strftime("%b")
        year_number = datetime.today().strftime("%Y")
        month_text = month_text.lower()

        # First we get the short version of the month name, used for finding.
        month_short_correct = re.findall(rf'<tr id="{month_text}"   >.*?<td>(.*?)<span class="NoMo">', page_text,
                                         flags=re.DOTALL)
        # print(f"Month Short {month_short_correct}")

        # {month_text} Example output: september
        # We find the perfect day of the given month.
        fullmoon_date = re.findall(
            rf'<tr id="{month_text}"   >.*<td>{month_short_correct[0]} (.*?), {year_number}<br>..... ...</td>',
            page_text, flags=re.DOTALL)

        # Returns day of Month that its fullmoon.
        return fullmoon_date[0]
    else:
        # Get fullmoon of the given month.

        # If month is not in this year.
        if int(month) > 12:
            return "Next Year"

        # Gets given month.
        month_ = int(month)
        month_text = calendar.month_name[month_]
        # We don't handle next year. So yeah.
        year_number = datetime.today().strftime("%Y")
        month_text = month_text.lower()

        # First we get the short version of the month name, used for finding.
        month_short_correct = re.findall(rf'<tr id="{month_text}"   >.*?<td>(.*?)<span class="NoMo">', page_text,
                                         flags=re.DOTALL)
        # print(f"Month Short {month_short_correct}")

        # {month_text} Example output: september
        # We find the perfect day of the given month.
        fullmoon_date = re.findall(
            rf'<tr id="{month_text}"   >.*<td>{month_short_correct[0]} (.*?), {year_number}<br>..... ...</td>',
            page_text, flags=re.DOTALL)

        # Returns day of Month that its fullmoon.
        return fullmoon_date[0]


def is_fullmoon_over(day):
    """Returns a true or false based on if the fullmoon already passed."""
    day_current = datetime.today().strftime("%d")

    # Convert strings to number
    day = int(day)
    day_current = int(day_current)

    # Check if day has passed.
    if day > day_current:
        return False
    elif day < day_current:
        return True
    else:
        return False


def get_next_month(month):
    if int(month) > 12:
        month = int(month)
        month = month + 1
        # month = str(month)
        return month
    else:
        # Increase year
        # We don't handle such things yet.
        return month


def get_next_month_current():
    month = datetime.today().strftime("%m")
    if int(month) != 12:
        month = int(month) + 1
        month = str(month)
        return month
    else:
        # Increase year
        # We don't handle such things yet.
        return month


def get_current_date():
    """Returns current Date in format %d-%m-%Y"""
    today = datetime.today().strftime("%d-%m-%Y")
    return today


def get_current_month_text():
    """Returns the current Month as text."""
    month = int(datetime.today().strftime("%m"))
    month_ = calendar.month_name[month]
    return month_


def get_given_month_text(month):
    """Returns the given number Month as text."""
    if month == "Next Year":
        return "of Next Year"
    month = int(month)
    _month = calendar.month_name[month]
    return _month


def get_ending_day(number):
    """Returns naming end of a given number"""
    end_of_number = number[-1]
    if end_of_number == 1:
        return "st"
    elif end_of_number == 2:
        return "nd"
    elif end_of_number == 3:
        return "rd"
    else:
        return "th"


# Debugging
if __name__ == "__main__":
    # Used to test functions
    # print(get_current_moonphase())
    # print(get_c_mphase_image())
    print(get_fullmoon(13))
# print(is_fullmoon_over(10))
